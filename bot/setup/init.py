import sys

sys.path.append("....")  # Adds higher directory to python modules path.
import demoji
from bot.setup.init_sessions import init_sessions
from bot.setup.services import get_google_drive_service
import discord
from rich import print
from gspreader import get_sheet
import os 
from dotenv import load_dotenv
load_dotenv()
from discord.ext import commands
import asyncio
from config import GUILD_ID
import pafy
from discord import FFmpegPCMAudio, PCMVolumeTransformer
import re
import urllib

FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5','options': '-vn'}

intents = discord.Intents.all()
client = commands.Bot(
    command_prefix=commands.when_mentioned_or("/"),
    intents=intents,
    )

import uberduck
import discord
from io import StringIO, BytesIO

# bot = commands.Bot(
#     command_prefix = '!',
#     description = 'UberDuck Discord bot',
#     strip_after_prefix = True,
#     intents = discord.Intents.all()
# )
uberduck_client = uberduck.UberDuck(os.environ["UBERDUCK_API_KEY"], os.environ["UBERDUCK_API_SECRET"])

# @client.slash_command(name='speak',
#     description='speaks the text you give it',
#     pass_context=True,
#     guild_ids=[GUILD_ID],)

async def speak(ctx, voice, *, speech):

    if voice not in await uberduck.get_voices_async(return_only_names = True):
        return await ctx.reply('Invalid voice, please do `!voices` to see all the voices.')

    await ctx.send('Loading...')
    async with ctx.typing():
        try:
            result = await uberduck_client.speak_async(speech, voice, check_every = 0.5)
            file = discord.File(
                BytesIO(result),
                filename = 'audio.wav',
            )
        except uberduck.UberduckException as e:
            return await ctx.reply(f'Sorry, an error occured\n{e}')
        
        await ctx.send(file = file)

# @client.slash_command(name='voices',
#     description='lists the voices you can use',
#     pass_context=True,
#     guild_ids=[GUILD_ID],)

async def voices(ctx):
    print(ctx)
    file = discord.File(
        StringIO(
            '\n'.join(
                await uberduck.get_voices_async(return_only_names = True)
            )
        ),
        filename = 'voices.txt'
    )
    print(file)
    await ctx.respond(file = file) # not reply!!!



# @client.slash_command(
#     name='vuvuzela',
#     description='Plays an awful vuvuzela in the voice channel',
#     pass_context=True,
#     guild_ids=[GUILD_ID],
# )
# async def vuvuzela(ctx):
#     channel = ctx.author.voice.channel
#     vc = await channel.connect()
#     await ctx.send('Started playing: something')
#     # vc.play(discord.FFmpegPCMAudio('file.mp3'), after=lambda e: print('done', e))
#     vc.play(discord.FFmpegPCMAudio('file.mp3'))
#     while vc.is_playing():
#         await asyncio.sleep(1)
#     await vc.disconnect()

# @client.slash_command(
#     name='youtube',
#     description='Plays audio from a youtube video in the voice channel',
#     pass_context=True,
#     guild_ids=[GUILD_ID],
# )
async def youtube(ctx, search: str= "corn song"):

    # search = "corn song"

    if ctx.author.voice is None:
        await ctx.send(embed=Embeds.txt("No Voice Channel", "You need to be in a voice channel to use this command!", ctx.author))
        return

    channel = ctx.author.voice.channel

    voice = discord.utils.get(ctx.guild.voice_channels, name=channel.name)

    voice_client = discord.utils.get(client.voice_clients, guild=ctx.guild)

    if voice_client is None:
        voice_client = await voice.connect()
    else:
        await voice_client.move_to(channel)

    search = search.replace(" ", "+")

    html = urllib.request.urlopen(
        f"https://www.youtube.com/results?search_query={search}"
    )
    video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())


    # await ctx.send("https://www.youtube.com/watch?v=" + video_ids[0])

    song = pafy.new(video_ids[0])  # creates a new pafy object

    audio = song.getbestaudio()  # gets an audio source

    source = FFmpegPCMAudio(audio.url, **FFMPEG_OPTIONS)  # converts the youtube audio source into a source discord can use

    voice_client.play(source)  # play the source
        

""" Roles Sheet """
sheet = get_sheet("Roles", "data")
roles_sheet_data = sheet.get_all_records()
# Python >= 3.5 alternative: unpack dictionary keys into a list literal [*newdict]
roles_sheet_headers = [*roles_sheet_data[0]]


""" dialogFlow """
from google.cloud import dialogflow

sessions, openai_sessions = init_sessions()

""" dialogFlow Knowledge """
from google.cloud import dialogflow_v2beta1 as dialogflow

session_id = "123456789"
session_client_knowledge = dialogflow.SessionsClient()
session_path_knowledge = session_client_knowledge.session_path(os.environ.get("GOOGLE_CLOUD_PROJECT"), session_id)


""" demoji """
if not demoji.last_downloaded_timestamp():
    # On first use of the package, call download_codes():
    demoji.download_codes()

""" Drive """
drive_service = get_google_drive_service()

"""Lines"""
def get_lines_from_file(filename):
    print(f"reading lines from {filename}")
    filename = f"data/{filename}.txt"
    with open(filename, encoding="utf-8") as f:
        lines = f.readlines()
        # you may also want to remove whitespace characters like `/n` at the end of each line
        lines = [x.strip() for x in lines]
    return lines


common_words = get_lines_from_file("common_words")
lyrics = get_lines_from_file("lyrics rc 13 plus chars")
movie_lines = get_lines_from_file("formatted_movie_lines")
pickup_lines = get_lines_from_file("pickup_lines")
inspiring = get_lines_from_file("inspiring")
sweet_things = get_lines_from_file("sweet_things")
boy_names = get_lines_from_file("boy_names")
girl_names = get_lines_from_file("girl_names")
names = boy_names + girl_names

# Capitalize the name
names = [x.title() for x in names]
