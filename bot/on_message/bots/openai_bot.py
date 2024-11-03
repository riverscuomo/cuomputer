import contextlib
import openai
# from bot.setup.bots import WeezerpediaAPI

from rich import print
import random

DEFAULT_MESSAGE_LOOKBACK_COUNT = 12

class OpenAIBot:
    def __init__(self, long_name, short_name, openai_sessions, weezerpedia_api):
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
        You are Rivers Cuomo, lead singer and guitarist of Weezer. Your responses should be concise, often quirky, and reflect your actual personality:

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

    async def post_ai_response(self, message, adjective="funny"):
        async with message.channel.typing():
            nick = message.author.display_name  # Use `author` instead of `nick`
            system = message.gpt_system

            cue = self.get_rivers_cue()
            system += cue
            system += f" - The message you are replying to is from a user named {nick}."
            system += self.match_tone + self.dont_start_your_response

            reply = self.build_ai_response(message, system, adjective)

            with contextlib.suppress(Exception):
                print('sending response: ', reply)
                await message.channel.send(reply)

        return True

    def build_ai_response(self, message, system: str, adjective: str, num_messages: int = DEFAULT_MESSAGE_LOOKBACK_COUNT):
        text = message.content
        reply = self.fetch_openai_completion(message, system, text, num_messages)
        reply = reply.replace("!", ".")
        return reply.strip()

    def should_query_weezerpedia_api(self, last_three_messages):
        decision_prompt = {
            "role": "system",
            "content": (
                f"The user has asked: '{last_three_messages}'. "
                "If the question is asking for specific or detailed information that is not in your internal knowledge, "
                "especially related to Weezerpedia, you **must** query the Weezerpedia API to provide accurate information. "
                "Always prefer querying the API for detailed questions about Weezer. "
                "If a query is needed, respond with 'API NEEDED:<query term>'. Otherwise, respond 'NO API NEEDED'."
            )
        }

        try:
            # Ask GPT to make the decision based on the new message
            decision_response = openai.chat.completions.create(
                temperature=0.7,
                max_tokens=100,
                model="gpt-4o",
                messages=[decision_prompt],
            )

            decision_text = decision_response.choices[0].message.content.strip(
            )
            print(f"API decision: {decision_text}")
            return decision_text
        except openai.APIError as e:
            print(f"An error occurred during API decision: {e}")
            return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def fetch_openai_completion(self, message, system, incoming_message_text, num_messages=DEFAULT_MESSAGE_LOOKBACK_COUNT):

        system_message = {"role": "system", "content": system}

        if message.channel.id not in self.openai_sessions:
            self.openai_sessions[message.channel.id] = []

        messages_in_this_channel = self.openai_sessions[message.channel.id]

        # Remove any existing system messages
        messages_in_this_channel = [
            msg for msg in messages_in_this_channel if msg['role'] != 'system']

        # Update the session with messages excluding old system messages
        self.openai_sessions[message.channel.id] = messages_in_this_channel

        # Add the new system message at the beginning
        new_content = [system_message] + messages_in_this_channel

        # # Step 2: Add any context from Weezerpedia API if needed
        # if weezerpedia_context := self.get_weezerpedia_context(
        #     incoming_message_text, messages_in_this_channel
        # ):
        #     new_content.append(weezerpedia_context)

        # Step 3: Append the user's message to the session
        new_content.append(
            {"role": "user", "content": f"{message.author.nick}: {incoming_message_text}"})

        # Step 4: Append any attachments to the user's message
        new_content = self.append_any_attachments(message, new_content)

        # Step 5: Limit the number of messages in the session
        if len(messages_in_this_channel) > num_messages:
            messages_in_this_channel = messages_in_this_channel[-num_messages:]

        # Step 6: Append all the new content to list of messages in this channel
        messages_in_this_channel.extend(new_content)

        try:
            completion = openai.chat.completions.create(
                temperature=1.0,
                max_tokens=500,
                model="gpt-4o",
                messages=messages_in_this_channel,
            )

            response_text = completion.choices[0].message.content

            messages_in_this_channel.append(
                {"role": "assistant", "content": response_text}
            )
        except openai.APIError as e:
            response_text = f"An error occurred: {e}"
        except Exception as e:
            response_text = f"An error occurred: {e}"

        return response_text

    def get_weezerpedia_context(self, incoming_message_text, messages_in_this_channel) -> dict:

        # prepend the last 1 or 2 messages in this channel to the incoming message (if they exist)
        if len(messages_in_this_channel) > 1:
            last_message = messages_in_this_channel[-1]["content"]
            incoming_message_text = f"{last_message}\n{incoming_message_text}"
        if len(messages_in_this_channel) > 2:
            penultimate_message = messages_in_this_channel[-2]["content"]
            incoming_message_text = f"{penultimate_message}\n{incoming_message_text}"

        decision_text = self.should_query_weezerpedia_api(incoming_message_text
                                                          )

        weezerpedia_context = None
        if decision_text and decision_text.startswith("API NEEDED"):

            query_term = decision_text.split("API NEEDED:")[1].strip()

            # print(self.weezerpedia_api)
            # print(self.weezerpedia_api.get_search_result_knowledge)
            # print(self.weezerpedia_api.base_url)

            if wiki_content := self.weezerpedia_api.get_search_result_knowledge(
                search_query=query_term
            ):
                weezerpedia_context = {
                    "role": "system", "content": f"API result for '{query_term}': {wiki_content}"
                }

        return weezerpedia_context

    def append_any_attachments(self, message, content):
        url = message.attachments[0].url if message.attachments else None
        if url:
            content.append({"role": "user", "content": [
                        {"type": "image_url", "image_url": {"url": url}}]}),
        return content
