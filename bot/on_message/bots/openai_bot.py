import contextlib
from dataclasses import dataclass
import json
import os
from typing import Any, Optional
import openai
from bot.on_message.bots.weezerpedia import WeezerpediaAPI

from rich import print
import random

DEFAULT_MESSAGE_LOOKBACK_COUNT = 15


@dataclass(frozen=True)
class PromptParams:
    system_prompt: str
    user_prompt: str
    user_name: str
    channel_id: int
    attachment_urls: list[str]


class OpenAIBot:
    def __init__(self, long_name: str, short_name: str, openai_sessions: list, weezerpedia_api: WeezerpediaAPI):
        self.long_name = long_name
        self.short_name = short_name
        self.openai_sessions = openai_sessions
        self.weezerpedia_api = weezerpedia_api
        self.introductory_info = " - You are in the middle of an ongoing conversation and do not need to provide introductory information."
        self.well_known_member = " - You are a well known member of this discord server."
        self.not_an_assistant = " - You are NOT an assistant. You are just another member of the server."
        self.kind = " - You are kind."
        self.be_terse = f" - Keep the responses SHORT. After all, {short_name} is naturally terse."
        self.stimulate = " -but try to keep the conversation going. Ask questions, make suggestions, and provide information. Be engaging and stimulating."
        self.lead = " - try to subtly lead the conversation to an uncommon SPECIFIC topic that the user would find very interesting."
        self.match_tone = " - Match the style and tone of the message you are replying to."
        self.dont_start_your_response = f" - Do not start your response with the indicator of who you are, such as '{long_name}: '. Just start with your response."
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

    async def post_ai_response(self, message, adjective="funny"):
        async with message.channel.typing():
            nick = message.author.display_name  # Use `author` instead of `nick`
            system = message.gpt_system

            cue = self.get_rivers_cue()
            system += cue
            system += f" - The message you are replying to is from a user named {nick}."
            system += self.match_tone + self.dont_start_your_response

            reply = await self.build_ai_response(
                message, system, adjective, DEFAULT_MESSAGE_LOOKBACK_COUNT)

            with contextlib.suppress(Exception):
                print('sending response: ', reply)
                await message.channel.send(reply)

        return True

    async def build_ai_response(self, message, system: str, adjective: str, num_messages_lookback: int):
        attachment_urls = [message.attachments[0].url
                           ] if message.attachments else []
        display_name = message.author.nick or message.author.name
        content = f"{display_name}: {message.content}"

        original_content, original_display_name = await self.get_optional_original_message_content_and_display_name(message)
        if original_content:
            content = f"Replying to: '{original_display_name}: {original_content}'\n\n{content}"

        prompt_params = PromptParams(user_prompt=content,
                                system_prompt=system,
                                channel_id=message.channel.id,
                                user_name=display_name,
                                attachment_urls=attachment_urls)

        reply = self.fetch_openai_completion(
            prompt_params, num_messages_lookback)
        reply = reply.replace("!", ".")
        return reply.strip()

    def _get_response_or_weezerpedia_function_call_results(self, new_content: list[dict[str, str]], function_call: bool) -> Optional[str]:
        try:
            completion = openai.chat.completions.create(
                temperature=0.7,
                max_tokens=100,
                model="gpt-4o",
                messages=new_content,
                functions = [
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
            response_text = f"An error occurred: {e}"
        except Exception as e:
            response_text = f"An error occurred: {e}"
        return response_text

    def fetch_openai_completion(self, prompt_params: PromptParams, num_messages_lookback: int):
        system_message = {"role": "system",
                          "content": prompt_params.system_prompt}

        if prompt_params.channel_id not in self.openai_sessions:
            self.openai_sessions[prompt_params.channel_id] = []

        messages_in_this_channel = self.openai_sessions[prompt_params.channel_id]

        # For testing purposes, if there are fewer than 5 messages in the channel, add some dummy messages

        # if running on heroku

        # Check if running in production
        is_production = os.getenv('ENV') == 'production'

        # For testing purposes, if there are fewer than 5 messages in the channel, add some dummy messages
        if not is_production and len(messages_in_this_channel) < 5:
            messages_in_this_channel = [
                {"role": "user", "content": "My favorite color is blue."},
                {"role": "user", "content": "My favorite color is red."},
                {"role": "user", "content": "My favorite color is yellow."},
                {"role": "user", "content": "My favorite color is green."},
                {"role": "user", "content": "My favorite color is orange."},
            ]

        # Remove any existing system messages
        new_content = [
            msg for msg in messages_in_this_channel if msg["role"] != "system" and "[INTERNAL]" not in msg["content"]]

        # Replace the channel messages with the cleaned up content
        self.openai_sessions[prompt_params.channel_id] = new_content

        # Append the user's message to the session
        new_content.append(
            {"role": "user", "content": prompt_params.user_prompt})

        # Append any attachments to the user's message
        self.append_any_images(prompt_params.attachment_urls, new_content)

        # Limit the number of messages in the session
        if len(new_content) > num_messages_lookback:
            new_content = new_content[-num_messages_lookback:]
        new_content = [system_message] + new_content

        function_call_response_text = self._get_response_or_weezerpedia_function_call_results(new_content, True)
        function_call_content =  [{"role": "user", "content": f"Incorporate the following Weezerpedia entry into your response, \
                                   to the extent it is relevant: \n {function_call_response_text}"}] if function_call_response_text else []
        new_content = new_content[:-1] + function_call_content + [new_content[-1]]  # make the user message we are responding to come last
        response_text = self._get_response_or_weezerpedia_function_call_results(new_content, False)
        new_content.append(
            {"role": "assistant", "content": response_text}
        )

        return response_text

    def append_any_images(self, attachment_urls: list[str], content: list[dict[str, Any]]):
        for url in attachment_urls:
            if any(ext in url for ext in ['.jpg', '.jpeg', '.png', '.gif']):
                content.append({"role": "user", "content": [
                    {"type": "image_url", "image_url": {"url": url}}]})
