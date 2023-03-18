import contextlib
import openai
from bot.setup.init import client
from bot.setup.init import openai_sessions
from config import cuomputer_id
import discord
from bot.scripts.message.finalize_response import finalize_response
from config import channels

import asyncio # required for the sleeping

import uberduck
from gtts import gTTS

from io import BytesIO

import os
uberduck_client = uberduck.UberDuck(os.environ["UBERDUCK_API_KEY"], os.environ["UBERDUCK_API_SECRET"])



async def post_gpt_response(nick: str, message, language_code: str, system = "you are Rivers Cuomo from Weezer. ", adjective: str="funny"):
    """
    Openai bot

    """
    print("post_gpt_response")
    # await client.process_commands(message)
    async with message.channel.typing():

        if message.channel.id == channels["dan"]:
            system = "you are Rivers Cuomo from Weezer but you have adopted the persona of a hyper-opinionated and knowledgable Weezer fan. "

        if message.channel.id == channels["geezerville"]:
            system = "you are Rivers Cuomo from Weezer. But you're not trying to act younger than you are (52). You're okay talking about middle-age issues including having kids. You sometimes reference 80's nostalgia. "
        
        system += f" You are in a conversation with a fan named {nick}."
        reply = build_openai_response(message, system, adjective)
        print(f"reply: {reply}")

        response = finalize_response(reply, language_code, nick, replace_names=True)
        print(f"response: {response}")

        # await read_message(message,response, language_code)

        # await asyncio.sleep(8)

        with contextlib.suppress(Exception):
            await message.channel.send(response)

        return True


async def read_message(message, response: str, language_code: str):
    print(f"read_message: {response} in {language_code}")     

    if language_code == "en":
        try:
            # https://app.uberduck.ai/leaderboard/voice
            result = await uberduck_client.speak_async(response, "Fluttershy", check_every = 0.5)
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

        print("not engligh so using gtts instead of uberduck")

        # get the text to speech
        tts = gTTS(response, lang=language_code)

        tts.save("file.txt")

    
    # await ctx.send(file = file)

    channel = client.get_channel(channels["lounge"])
    print(channel)

    vc = discord.utils.get(client.voice_clients, guild=message.guild)

    if vc is None:
        vc = await channel.connect()
    else:
        await vc.move_to(channel)

    
        vc.play(discord.FFmpegPCMAudio('file.txt'))
        while vc.is_playing():
            await asyncio.sleep(1)
    # await vc.disconnect()


def build_openai_response(text: str, system:str, adjective: str):

    # prompt = f"{prompt}.\nHere is the text I want you to respond to: '{text}'"

    prompt = f"{system}: respond in a {adjective}  way. Here is the user's message: {text}."

    # Get the open model from .env if the user has specified it.
    model = os.environ.get("OPENAI_MODEL")

    # Use gpt-3 if the model is not specified
    if model is None:
        model = "text-davinci-003"

    # Use gpt-4 if the model is specified as gpt-4
    if model == "gpt-4":
        print("Using gpt-4")

        completion = openai.ChatCompletion.create(model=model, messages=[{"role": "user", "content": prompt}])
        reply = completion.choices[0].message.content    

    # Otherwise use gpt-3 or another model specified in .env
    else:
        completion = openai.Completion.create(
            model=os.environ.get("OPENAI_MODEL"),
            prompt=prompt,
            temperature=1,
            max_tokens=120,
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



# def build_openai_response(message, adjective: str):
#     print("build_openai_response")
#     # c = message.content.split(" ")[1]
#     incoming_message = message.content
#     # channel_name = message.channel.name
#     # author_name = message.author.name

#     # print(message.author, message.author.id, message.author.name)
#     # if message.author.id != cuomputer_id:
#     #     print('adding context to openai session')

#     # try:
#     #     openai_sessions[channel_name][message.author.name] += f" {incoming_message}"
#     # # rarely, a new channel will be created and the bot will not have a session for it yet
#     # except KeyError:
#     #     openai_sessions[channel_name][message.author.name] = incoming_message
#     # context = openai_sessions[channel_name][message.author.name] 

    

#     # context = manage_session_context(message, channel_name, )
#     context = incoming_message

#     prompt = f"write a response for Rivers Cuomo in this conversation in a {adjective}  way: {context}."
#     # print(c)
#     reply = openai.Completion.create(
#         model="text-davinci-003",
#         prompt=prompt,
#         temperature=1.0, # higher is more creative, lower is more boring
#         max_tokens=200, # speech tokens, not characters
#     )
#     reply = reply["choices"]
#     # print(reply)
#     reply = reply[0]["text"]
#     print(f"reply={reply}")

#     reply = reply.replace("Rivers Cuomo: ", "").replace("Rivers Cuomo:", "")
#     reply = reply.replace("\n\n", "\n")
#     reply = reply.replace('"', "")
#     reply = reply.strip()
    
#     return reply


def manage_session_context(message, channel_name, author_name, incoming_message):
    """ If you want to keep track of the context for each channel, use this function. Downside is that it may use more of your open ai token allowance."""

    try:
        openai_sessions[channel_name] += f" {author_name}: {incoming_message}"

    # rarely, a new channel will be created and the bot will not have a session for it yet
    except KeyError:
        openai_sessions[channel_name] = incoming_message
    context = openai_sessions[channel_name] 

    print('\n\n')
    print(f"context for openai-bot in channel {channel_name} is {len( context)} characters long")
    print(context)
    print('\n\n')

    # truncate the context to 150 characters
    if len(context ) > 100:
        openai_sessions[message.channel.name] = openai_sessions[message.channel.name][-100:]
    return context

