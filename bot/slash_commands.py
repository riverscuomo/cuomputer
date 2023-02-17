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