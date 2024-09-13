# from setup.init import client
# from config import GUILD_ID
# import discord
# import asyncio

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
