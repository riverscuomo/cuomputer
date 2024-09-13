# import asyncio
# import os
# from google.cloud import dialogflow_v2beta1 as dialogflow
# from google.cloud import dialogflow
# import pytz
# from io import StringIO, BytesIO
# import uberduck
# import urllib
# import re
# from discord import FFmpegPCMAudio
# import pafy
# from discord.ext import commands
# from dotenv import load_dotenv
# from gspreader import get_sheet
# from rich import print
# import discord
# from bot.setup.services.google_services import get_google_drive_service
# from bot.setup.services.init_sessions import init_sessions
# import demoji
# import sys
# from config import TOKEN

# sys.path.append("....")  # Adds higher directory to python modules path.
# load_dotenv()

# FFMPEG_OPTIONS = {
#     'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

# intents = discord.Intents.all()
# client = commands.Bot(
#     command_prefix=commands.when_mentioned_or("/"),
#     intents=intents,
#     allowed_mentions=discord.AllowedMentions(roles=False, everyone=False),
# )

# tz = pytz.timezone('America/Los_Angeles')


# async def youtube(ctx, search: str = "corn song"):

#     # search = "corn song"

#     if ctx.author.voice is None:
#         await ctx.send(embed=Embeds.txt("No Voice Channel", "You need to be in a voice channel to use this command!", ctx.author))
#         return

#     channel = ctx.author.voice.channel

#     voice = discord.utils.get(ctx.guild.voice_channels, name=channel.name)

#     voice_client = discord.utils.get(client.voice_clients, guild=ctx.guild)

#     if voice_client is None:
#         voice_client = await voice.connect()
#     else:
#         await voice_client.move_to(channel)

#     search = search.replace(" ", "+")

#     html = urllib.request.urlopen(
#         f"https://www.youtube.com/results?search_query={search}"
#     )
#     video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())

#     # await ctx.send("https://www.youtube.com/watch?v=" + video_ids[0])

#     song = pafy.new(video_ids[0])  # creates a new pafy object

#     audio = song.getbestaudio()  # gets an audio source

#     # converts the youtube audio source into a source discord can use
#     source = FFmpegPCMAudio(audio.url, **FFMPEG_OPTIONS)

#     voice_client.play(source)  # play the source


# """ Roles Sheet """
# sheet = get_sheet("Roles", "data")
# roles_sheet_data = sheet.get_all_records()
# # Python >= 3.5 alternative: unpack dictionary keys into a list literal [*newdict]
# roles_sheet_headers = [*roles_sheet_data[0]]


# """ dialogFlow """

# sessions, openai_sessions = init_sessions()

# """ dialogFlow Knowledge """

# session_id = "123456789"
# session_client_knowledge = dialogflow.SessionsClient()
# session_path_knowledge = session_client_knowledge.session_path(
#     os.environ.get("GOOGLE_CLOUD_PROJECT"), session_id)


# """ demoji """
# if not demoji.last_downloaded_timestamp():
#     # On first use of the package, call download_codes():
#     demoji.download_codes()

# """ Drive """
# drive_service = get_google_drive_service()

# """Lines"""


# def get_lines_from_file(filename):
#     print(f"reading lines from {filename}")
#     filename = f"data/{filename}.txt"
#     with open(filename, encoding="utf-8") as f:
#         lines = f.readlines()
#         # you may also want to remove whitespace characters like `/n` at the end of each line
#         lines = [x.strip() for x in lines]
#     return lines


# common_words = get_lines_from_file("common_words")
# lyrics = get_lines_from_file("lyrics rc 13 plus chars")
# movie_lines = get_lines_from_file("formatted_movie_lines")
# pickup_lines = get_lines_from_file("pickup_lines")
# inspiring = get_lines_from_file("inspiring")
# sweet_things = get_lines_from_file("sweet_things")
# boy_names = get_lines_from_file("boy_names")
# girl_names = get_lines_from_file("girl_names")
# names = boy_names + girl_names

# # Capitalize the name
# names = [x.title() for x in names]
