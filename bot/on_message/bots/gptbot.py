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



async def post_gpt_response(nick: str, message, language_code: str, adjective: str="funny"):
    """
    Openai bot

    """
    print("post_gpt_response")
    # await client.process_commands(message)
    async with message.channel.typing():
        
        reply = build_openai_response(message, adjective)
        print(f"reply: {reply}")

        response = finalize_response(reply, language_code, nick, replace_names=True)
        print(f"response: {response}")

        await read_message(message,response, language_code)

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

def build_openai_response(message, adjective: str):
    print("build_openai_response")
    # c = message.content.split(" ")[1]
    incoming_message = message.content
    # channel_name = message.channel.name
    # author_name = message.author.name

    # print(message.author, message.author.id, message.author.name)
    # if message.author.id != cuomputer_id:
    #     print('adding context to openai session')

    # try:
    #     openai_sessions[channel_name][message.author.name] += f" {incoming_message}"
    # # rarely, a new channel will be created and the bot will not have a session for it yet
    # except KeyError:
    #     openai_sessions[channel_name][message.author.name] = incoming_message
    # context = openai_sessions[channel_name][message.author.name] 

    

    # context = manage_session_context(message, channel_name, )
    context = incoming_message

    prompt = f"write a response for Rivers Cuomo in this conversation in a {adjective}  way: {context}."
    # print(c)
    reply = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=1.0, # higher is more creative, lower is more boring
        max_tokens=200, # speech tokens, not characters
    )
    reply = reply["choices"]
    # print(reply)
    reply = reply[0]["text"]
    print(f"reply={reply}")

    reply = reply.replace("Rivers Cuomo: ", "").replace("Rivers Cuomo:", "")
    reply = reply.replace("\n\n", "\n")
    reply = reply.replace('"', "")
    reply = reply.strip()
    
    return reply


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

