import contextlib
import openai
from litellm import completion
from bot.setup.init import client
from bot.setup.init import openai_sessions
from config import cuomputer_id
import discord
from bot.scripts.message.finalize_response import finalize_response
from config import channels

import asyncio  # required for the sleeping

import uberduck
from gtts import gTTS

from io import BytesIO

import os
uberduck_client = uberduck.UberDuck(
    os.environ["UBERDUCK_API_KEY"], os.environ["UBERDUCK_API_SECRET"])


async def post_gpt_response(message, system="you are Rivers Cuomo from Weezer. ", adjective: str = "funny"):
    """
    Openai bot

    """
    print("post_gpt_response")
    print(openai_sessions[message.channel.id])
    # await client.process_commands(message)
    async with message.channel.typing():

        system = system.replace(" from Weezer", "")
        system += "You are in the middle of an ongoing conversation and do not need to provide introductory information. You are a well known member of this discord server."
        system += f" The message you are replying to is from a fan named {message.nick}."
        reply = build_openai_response(message, system, adjective)
        # print(f"reply: {reply}")

        response = finalize_response(
            reply, message.language_code, message.nick, replace_names=True)
        print(f"response: {response}")

        await read_message(message, response)

        # await asyncio.sleep(8)

        with contextlib.suppress(Exception):
            await message.channel.send(response)

        # # add the message and the reponse to the session context
        # manage_session_context(message, message.channel.name, message.nick, message.content)

        return True


def build_openai_response(message, system: str, adjective: str):
    text = message.content

    # prompt = f"{prompt}.\nHere is the text I want you to respond to: '{text}'"

    system += f" Make your response {adjective}."
    system += "Don't start your response with the indicator of who you are, such as 'Rivers Cuomo: '. Just start with your response."

    # prompt = f"{text}."

    # Get the open model from .env if the user has specified it.
    model = os.environ.get("OPENAI_MODEL")

    # Use gpt-3 if the model is not specified
    if model is None:
        model = "text-davinci-003"

    # Use gpt-4 if the model is specified as gpt-4
    if model == "gpt-4":
        reply = fetch_gpt4_completion(message, system, text, model)
    else:
        completion = completion(
            model=os.environ.get("OPENAI_MODEL"),
            prompt=text,
            temperature=1,
            max_tokens=80,
        )
        reply = completion["choices"]
        reply = reply[0]["text"]

    # whatever the model was, now you can make a few universal changes to the response.
    reply = reply.replace("\n\n", "\n")
    reply = reply.replace('"', "")
    reply = reply.replace("2020", "2023")
    reply = reply.replace("2021", "2023")
    reply = reply.strip()
    return reply


def fetch_gpt4_completion(message, system, text, model):
    print("Using gpt-4")
    # print(f"system: {system}")
    # print(f"text: {text}")

    # The first message is the system information
    messages = [{"role": "system", "content": system}]

    # Add the user's text to the openai session for this channel
    openai_sessions[message.channel.id].append(
        {"role": "user", "content": f"{message.author.name}: {text}"})

    # Limit the number of messages in the session to 6
    if len(openai_sessions[message.channel.id]) > 6:

        openai_sessions[message.channel.id] = openai_sessions[message.channel.id][-3:]

    # add all the messages from this channel to the system message
    messages.extend(openai_sessions[message.channel.id])
    # print(f"messages: {messages}")
    for m in messages:
        print(m)

    completion = completion(
        temperature=1.0,
        max_tokens=100,
        model=model,
        messages=messages,
        # "top_p": 1,
        # "frequency_penalty": 0.0,
        # "presence_penalty": 0.0,
        # stop=["\n", " Human:", " AI:"], # kills poems

    )
    text = completion.choices[0].message.content

    # add the response to the session. I suppose now there may be up to 7 messages in the session
    openai_sessions[message.channel.id].append(
        {"role": "assistant", "content": text})

    return text


async def read_message(message, response: str):
    print(f"read_message: {response} (in {message.language_code})")

    if message.language_code == "en":
        try:
            # https://app.uberduck.ai/leaderboard/voice
            result = await uberduck_client.speak_async(response, "Fluttershy", check_every=0.5)
            bytes_IO = BytesIO(result)

            # Create and open a readable file
            with open('file.txt', 'wb') as file:
                file.write(bytes_IO.read())
            # create
        except uberduck.UberduckException as e:
            # return await ctx.reply(f'Sorry, an error occured\n{e}')
            print(e)
            return

    else:

        print("not english so using gtts instead of uberduck")

        # get the text to speech
        tts = gTTS(response, lang=message.language_code)

        tts.save("file.txt")

    # await ctx.send(file = file)

    # Get the lounge channel
    channel = client.get_channel(channels["lounge"])
    print(channel)

    # Get the voice client for this server
    vc = discord.utils.get(client.voice_clients, guild=message.guild)

    if vc is None:
        vc = await channel.connect()
    else:
        await vc.move_to(channel)

    vc.play(discord.FFmpegPCMAudio('file.txt'))
    while vc.is_playing():
        await asyncio.sleep(1)
    # await vc.disconnect()


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
