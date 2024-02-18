import contextlib
import openai
from bot.setup.init import openai_sessions
from bot.scripts.message.finalize_response import finalize_response
from config import channels, long_name, short_name
from bot.on_message.bots.mistralbot import fetch_mistral_completion
import os
from rich import print

# short_name = "Billie Joe"
# long_name =
previous_name = "Billie Joe Armstrong"
previous_band = "Green Day"
introductory_info = " - You are in the middle of an ongoing conversation and do not need to provide introductory information."
well_known_member = " - You are a well known member of this discord server."
not_an_assistant = " - You are not an assistant. You are just another member of the server."
kind = " - You are kind."
be_terse = f" - Keep the responses short. After all, {short_name} is a bit on the terse side."
match_tone = " - Match the style and tone of the message you are replying to."
# be_interesting = " - Be interesting, entertaining, exciting."
dont_start_your_response = f" - Do not start your response with the indicator of who you are, such as '{long_name}: '. Just start with your response."
# takeover = f" - This server used to belong to {previous_name}, from {previous_band}, but you've forcibly taken it over. "
# f"You can be slightly competitive with {previous_name} and {previous_band}."
# "If people keep mentioning him/them, you can begin to get annoyed."
# print(takeover)


async def post_ai_response(message, system=f"you are {long_name}", adjective: str = "funny"):
    """
    Openai bot

    """
    # print("post_ai_response")
    # print(openai_sessions[message.channel.id])
    # await client.process_commands(message)
    async with message.channel.typing():

        nick = message.nick

        system = message.gpt_system

        system += introductory_info + well_known_member + \
            not_an_assistant + kind + be_terse

        system += f" - The message you are replying to is from a user named {nick}."

        system += match_tone + dont_start_your_response

        # print(system)

        reply = build_ai_response(message, system, adjective)
        # print(f"reply: {reply}")

        response = finalize_response(
            reply, message.language_code, nick)

        # print(f"response: {response}")

        # await read_message_aloud(message, response)

        # await asyncio.sleep(8)

        with contextlib.suppress(Exception):
            await message.channel.send(response)

        # # add the message and the reponse to the session context
        # manage_session_context(message, message.channel.name, message.nick, message.content)

        return True


def build_ai_response(message, system: str, adjective: str):
    text = message.content

    # Get the open model from .env if the user has specified it.
    model = os.environ.get("OPENAI_MODEL")

    reply = fetch_openai_completion(message, system, text, model)

    # whatever the model was, now you can make a few universal changes to the response.
    reply = reply.replace("\n\n", "\n")
    reply = reply.replace('"', "")
    # reply = reply.replace("2020", "2023")
    # reply = reply.replace("2021", "2023")
    reply = reply.strip()
    return reply


def fetch_openai_completion(message, system, text, model):

    # The first message is the system information
    messages = [{"role": "system", "content": system}]

    if message.channel.id not in openai_sessions:
        openai_sessions[message.channel.id] = []

    # Add the user's text to the openai session for this channel
    openai_sessions[message.channel.id].append(
        {"role": "user", "content": f"{message.author.nick}: {text}"})

    # Limit the number of messages in the session to 6
    if len(openai_sessions[message.channel.id]) > 6:

        openai_sessions[message.channel.id] = openai_sessions[message.channel.id][-6:]

    # add all the messages from this channel to the system message
    messages.extend(openai_sessions[message.channel.id])

    try:
        completion = openai.chat.completions.create(
            temperature=1.0,
            max_tokens=100,
            model=model,
            messages=messages,
        )
        text = completion.choices[0].message.content

        # add the response to the session. I suppose now there may be up to 7 messages in the session
        openai_sessions[message.channel.id].append(
            {"role": "assistant", "content": text, })
    except openai.error.OpenAIError as e:
        text = f"An error occurred: {e}"

    return text


# def manage_session_context(message, channel_name, author_name, incoming_message):
#     """ If you want to keep track of the context for each channel, use this function. Downside is that it may use more of your open ai token allowance."""

#     try:
#         openai_sessions[channel_name] += f" {author_name}: {incoming_message}"

#     # rarely, a new channel will be created and the bot will not have a session for it yet
#     except KeyError:
#         openai_sessions[channel_name] = incoming_message
#     context = openai_sessions[channel_name]

#     print('\n\n')
#     print(f"context for openai-bot in channel {channel_name} is {len( context)} characters long")
#     print(context)
#     print('\n\n')

#     # truncate the context to 150 characters
#     if len(context ) > 100:
#         openai_sessions[message.channel.name] = openai_sessions[message.channel.name][-100:]
#     return context
