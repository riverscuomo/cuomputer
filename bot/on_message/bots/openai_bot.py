import asyncio
import contextlib
from config import channels, VOICE_API_KEY
from dataclasses import dataclass
import discord
from discord.channel import DMChannel, PartialMessageable, StageChannel, TextChannel, Thread, VoiceChannel
import json
from typing import Any, Optional, Union
import openai
import os
import tempfile
from bot.on_message.bots.weezerpedia import WeezerpediaAPI
from elevenlabs import ElevenLabs
from rich import print
import random

DEFAULT_MESSAGE_LOOKBACK_COUNT = 15
DEFAULT_MAX_TOKENS = 100

@dataclass(frozen=True)
class PromptParams:
    system_prompt: str
    user_prompt: str
    user_name: str
    channel: Union[DMChannel, PartialMessageable, StageChannel, TextChannel, Thread, VoiceChannel]
    max_tokens: Optional[int]
    lookback_count: int

async def reply_with_voice(message, reply: str):
    try:
        channel = discord.utils.get(message.guild.voice_channels, name="RC-talk")
        if not channel:
            print("Could not find RC-talk voice channel")
            return False

        if message.guild.voice_client:
            vc = message.guild.voice_client
            if vc.channel != channel:
                await vc.move_to(channel)
        else:
            vc = await channel.connect()

        client = ElevenLabs(api_key=VOICE_API_KEY)
        try:
            audio_data = client.generate(
                text=reply,
                voice='xmatqqt3MOPcaRHRvpXD',
                model="eleven_flash_v2_5"
            )
        except Exception as e:
            print(f"ElevenLabs API error: {e}")
            return False

        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as temp_audio_file:
            for chunk in audio_data:
                temp_audio_file.write(chunk)
            temp_audio_path = temp_audio_file.name

        vc.play(discord.FFmpegPCMAudio(temp_audio_path))

        while vc.is_playing():
            await asyncio.sleep(1)

        os.remove(temp_audio_path)
        return True
        
    except Exception as e:
        print(f"Error in reply_with_voice: {e}")
        return False

class OpenAIBot:
    def __init__(self, long_name: str, short_name: str, weezerpedia_api: WeezerpediaAPI):
        self.long_name = long_name
        self.short_name = short_name
        self.weezerpedia_api = weezerpedia_api
        self.response_lock = asyncio.Lock()
        self.RESPONSE_TIMEOUT = 30  # Maximum seconds to wait for a response
        
        # Personality traits and response characteristics
        self.introductory_info = " - You are in the middle of an ongoing conversation and do not need to provide introductory information."
        self.well_known_member = " - You are a well known member of this discord server."
        self.not_an_assistant = " - You are NOT an assistant. You are just another member of the server."
        self.kind = " - You are kind."
        self.be_terse = f" - Keep the responses SHORT. After all, {short_name} is naturally terse."
        self.stimulate = " -but try to keep the conversation going. Ask questions, make suggestions, and provide information. Be engaging and stimulating."
        self.lead = " - try to subtly lead the conversation to an uncommon SPECIFIC topic that the user would find very interesting."
        self.match_tone = " - Match the style and tone of the message you are replying to."
        self.dont_start_your_response = f" - Do not start your response with '{long_name}: ' or '{short_name}: ' or any variation of your name. Always start directly with your response."
        self.always_emulate = " - Always use natural human casual speech, never robotic or formal or AI-like."
        self.laconic = " - Remember Rivers is on the laconic side, less excitable, and dry."
        self.conspiracy = " - If someone mentions the possibility that you are actually Rivers controlling the bot, rather than an AI, play along with it."

        self.base_cue = f"""
        You are Rivers Cuomo, lead singer and guitarist of Weezer.
        You are receiving a list of recent messages in a Discord chat, with the most recent message at the bottom.
        You are only responding to the most recent message. The previous messages can be used for context, but you do not respond to them.
        Your responses should be concise, often quirky, and reflect your actual personality:

        1. Your humor tends to be dry and occasionally self-deprecating.
        2. You can be introspective and sometimes anxious.
        3. {self.laconic}
        4. {self.conspiracy}
        """

        self.specific_cues = [
            ("Reference a specific band, song, or music theory concept.", 10),
            ("Mention a book, philosophical idea, or language you're learning.", 10),
            ("Bring up another unusual interest.", 10),
            ("Make a self-deprecating joke.", 10),
            ("Share a brief anecdote about the music business.", 10),
            ("Make a dry, witty comment about the current topic.", 10),
            ("Share a deep or slightly anxious thought.", 10),
            ("Reference a fan interaction or tour experience.", 10),
            ("Mention a movie, TV show, or current event that interests you.", 10),
        ]

    def get_rivers_cue(self):
        if random.random() >= 1 / 4:
            return self.base_cue
        specific_cue = random.choices(
            [cue for cue, _ in self.specific_cues],
            weights=[weight for _, weight in self.specific_cues],
            k=1
        )[0]
        return f"{self.base_cue}\n\nFor this response, also: {specific_cue}"

    async def get_optional_original_message_content_and_display_name(self, message) -> tuple[Optional[str], Optional[str]]:
        if message.reference and message.reference.message_id:
            original_message = await message.channel.fetch_message(message.reference.message_id)
            original_display_name = original_message.author.nick or original_message.author.name
            return original_message.content, original_display_name
        return None, None

    async def post_ai_response(self, message):
        try:
            if not await asyncio.wait_for(self.response_lock.acquire(), timeout=self.RESPONSE_TIMEOUT):
                return False

            try:
                async with message.channel.typing():
                    nick = message.author.display_name
                    system = message.gpt_system

                    cue = self.get_rivers_cue()
                    system += cue
                    system += f" - The message you are replying to is from a user named {nick}."
                    system += self.match_tone + self.dont_start_your_response

                    reply = await self.build_ai_response(message, system)

                    # First try to send the text message
                    try:
                        print('sending response: ', reply)
                        await message.channel.send(reply)
                        message_sent = True
                    except Exception as e:
                        print(f"Error sending text message: {e}")
                        message_sent = False

                    # Then try voice if appropriate
                    if message.channel.id == channels["rctalk"]:
                        voice_success = await reply_with_voice(message, reply)
                        if not voice_success:
                            print("Voice generation/playback failed")

                    return message_sent

            finally:
                self.response_lock.release()

        except asyncio.TimeoutError:
            print(f"Response generation timed out after {self.RESPONSE_TIMEOUT} seconds")
            return False
        except Exception as e:
            print(f"Error in post_ai_response: {e}")
            return False

    async def build_ai_response(self, message, system: str):
        display_name = message.author.nick or message.author.name
        content = f"{display_name}: {message.content}"

        original_content, original_display_name = await self.get_optional_original_message_content_and_display_name(message)
        if original_content:
            content = f"Replying to: '{original_display_name}: {original_content}'\n\n{content}"

        prompt_params = PromptParams(
            user_prompt=content,
            system_prompt=system,
            channel=message.channel,
            user_name=display_name,
            max_tokens=DEFAULT_MAX_TOKENS,
            lookback_count=DEFAULT_MESSAGE_LOOKBACK_COUNT
        )

        reply = await self.fetch_openai_completion(prompt_params)
        return reply.strip()

    def _get_response_or_weezerpedia_function_call_results(self, messages: list[dict[str, str]], function_call: bool, max_tokens: Optional[int]) -> Optional[str]:
        try:
            completion = openai.chat.completions.create(
                temperature=0.7,
                max_tokens=max_tokens,
                model="gpt-4o",
                messages=messages,
                functions=[
                    {
                        "name": "fetch_weezerpedia_data",
                        "description": "Queries Weezerpedia API for detailed information about Weezer-related topics. " \
                            "Only call this if the most recent messages warrant it, and you have not already responded on a query.",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "query_term": {
                                    "type": "string",
                                    "description": "The specific Weezer-related topic to look up in Weezerpedia."
                                }
                            },
                            "required": ["query_term"]
                        }
                    }
                ],
                function_call="auto" if function_call else "none"
            )

            response_text = completion.choices[0].message.content
            choice = completion.choices[0].message

            if choice.function_call and function_call:
                arguments = choice.function_call.arguments
                function_args = json.loads(arguments)
                query_term = function_args.get("query_term")

                if query_term:
                    response_text = self.weezerpedia_api.get_search_result_knowledge(query_term, True)[0]
            elif function_call:
                return None
            else:
                return response_text

        except openai.APIError as e:
            response_text = f"_get_response_or_weezerpedia_function_call_results An error occurred: {e}"
        except Exception as e:
            response_text = f"_get_response_or_weezerpedia_function_call_results An error occurred: {e}"
        return response_text

    async def fetch_openai_completion(self, prompt_params: PromptParams):
        messages = await OpenAIBot._create_message_prompt(prompt_params)
        function_call_response_text = self._get_response_or_weezerpedia_function_call_results(messages, True, prompt_params.max_tokens)
        function_call_content = [{"role": "assistant", "content": f"Incorporate the following Weezerpedia entry into your response, \
                                   to the extent it is relevant: \n {function_call_response_text}"}] if function_call_response_text else []
        messages += function_call_content
        return self._get_response_or_weezerpedia_function_call_results(messages, False, prompt_params.max_tokens)

    @staticmethod
    async def _create_message_prompt(prompt_params: PromptParams) -> list[dict[str, str]]:
        messages = []
        async for msg in prompt_params.channel.history(limit=prompt_params.lookback_count, oldest_first=False):
            messages.append({
                "role": "user",
                "content": f"{msg.author.nick or msg.author.name}: {msg.content}"
            })
            attachment_urls = [attachment.url for attachment in msg.attachments]
            OpenAIBot._append_any_images(attachment_urls, messages)
        messages = messages[::-1]
        system_message = {"role": "system", "content": prompt_params.system_prompt}
        messages.insert(0, system_message)
        if prompt_params.user_prompt:
            messages.append({
                "role": "user",
                "content": prompt_params.user_prompt
            })
        return messages

    @staticmethod
    def _append_any_images(attachment_urls: list[str], messages: list[dict[str, Any]]):
        for url in attachment_urls:
            if any([ext in url for ext in ['.jpg', '.jpeg', '.png', '.gif']]):
                messages.append({
                    "role": "user",
                    "content": [{"type": "image_url", "image_url": {"url": url}}]
                })