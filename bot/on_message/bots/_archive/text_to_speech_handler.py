from io import BytesIO
import random
import asyncio
from gtts import gTTS
import discord
from bot.setup.discord_bot import client
from config import channels
import uberduck
import os


class TextToSpeechHandler:
    def __init__(self):
        self.voices = uberduck.get_voices(return_only_names=True)
        self.uberduck_client = uberduck.UberDuck(
            os.environ["UBERDUCK_API_KEY"], os.environ["UBERDUCK_API_SECRET"]
        )

    async def read_message_aloud(self, message, response: str):
        print(f"read_message_aloud: {response} (in {message.language_code})")

        if message.language_code == "en":
            try:
                # Use random voice from Uberduck voices
                voice = random.choice(self.voices)
                print(f"voice: {voice}")
                result = await self.uberduck_client.speak_async(response, voice, check_every=0.5)
                bytes_io = BytesIO(result)

                # Create and open a readable file
                with open('file.txt', 'wb') as file:
                    file.write(bytes_io.read())
            except uberduck.UberduckException as e:
                print(e)
                print("Uberduck failed, using gTTS instead.")
                tts = gTTS(response, lang=message.language_code)
                tts.save('file.txt')
        else:
            print("Not English, using gTTS instead.")
            tts = gTTS(response, lang=message.language_code)
            tts.save('file.txt')

        await self.play_audio(message)

    async def play_audio(self, message):
        # Get the lounge channel
        voice_channel = client.get_channel(channels["lounge"])
        print(voice_channel)

        # Check if the bot is already connected to the correct voice channel
        vc = discord.utils.get(client.voice_clients, guild=message.guild)

        # If the bot is not connected or in another channel, connect or move to the correct channel
        if vc is None or not vc.is_connected() or vc.channel != voice_channel:
            if vc is not None and vc.is_connected():
                await vc.disconnect()  # Disconnect from the current channel if necessary
            vc = await voice_channel.connect()  # Connect to the correct voice channel

        # Before playing audio, create the audio source (ensure the file exists)
        audio_source = discord.FFmpegPCMAudio('file.txt')

        # Play audio only if not already playing
        if not vc.is_playing():
            vc.play(audio_source)

        # Wait for the audio to complete playing before returning
        while vc.is_playing():
            await asyncio.sleep(1)

# Example usage
# tts_handler = TextToSpeechHandler()
# await tts_handler.read_message_aloud(message, response)


# from io import BytesIO
# import random
# import asyncio
# from gtts import gTTS
# import discord
# from bot.setup.discord_bot import client
# from config import channels


# import uberduck


# import os
# voices = uberduck.get_voices(return_only_names=True)
# uberduck_client = uberduck.UberDuck(
#     os.environ["UBERDUCK_API_KEY"], os.environ["UBERDUCK_API_SECRET"])


# async def read_message_aloud(message, response: str):
#     print(f"read_message_aloud: {response} (in {message.language_code})")

#     if message.language_code == "en":
#         try:

#             # https://app.uberduck.ai/leaderboard/voice
#             voice = random.choice(voices)
#             print(f"voice: {voice}")
#             result = await uberduck_client.speak_async(response, voice, check_every=0.5)
#             bytes_IO = BytesIO(result)

#             # Create and open a readable file
#             with open('file.txt', 'wb') as file:
#                 file.write(bytes_IO.read())
#             # create
#         except uberduck.UberduckException as e:
#             # return await ctx.reply(f'Sorry, an error occured\n{e}')
#             print(e)
#             # return

#             print("uberduck failed so using gtts instead of uberduck")
#             # get the text to speech
#             tts = gTTS(response, lang=message.language_code)

#             tts.save("file.txt")

#     else:

#         print("not english so using gtts instead of uberduck")

#         # get the text to speech
#         tts = gTTS(response, lang=message.language_code)

#         tts.save("file.txt")

#     # await ctx.send(file = file)

#     # Get the lounge channel
#     voice_channel = client.get_channel(channels["lounge"])
#     print(voice_channel)

#     # Check if the bot is already connected to the correct voice channel
#     vc = discord.utils.get(client.voice_clients, guild=message.guild)

#     # If the bot is not connected or in another channel, connect or move to the correct channel
#     if vc is None or not vc.is_connected() or vc.channel != voice_channel:
#         if vc is not None and vc.is_connected():
#             await vc.disconnect()  # Disconnect from the current channel if necessary
#         vc = await voice_channel.connect()  # Connect to the correct voice channel

#     # Before playing audio, create the audio source (ensure the file exists)
#     # Update with the correct audio file path
#     audio_source = discord.FFmpegPCMAudio('file.txt')

#     # Play audio only if not already playing
#     if not vc.is_playing():
#         vc.play(audio_source)

#     # Wait for the audio to complete playing before returning
#     while vc.is_playing():
#         await asyncio.sleep(1)


# # bot = commands.Bot(
# #     command_prefix = '!',
# #     description = 'UberDuck Discord bot',
# #     strip_after_prefix = True,
# #     intents = discord.Intents.all()
# # )
# uberduck_client = uberduck.UberDuck(
#     os.environ["UBERDUCK_API_KEY"], os.environ["UBERDUCK_API_SECRET"])

# # @client.slash_command(name='speak',
# #     description='speaks the text you give it',
# #     pass_context=True,
# #     guild_ids=[GUILD_ID],)


# async def speak(ctx, voice, *, speech):

#     if voice not in await uberduck.get_voices_async(return_only_names=True):
#         return await ctx.reply('Invalid voice, please do `!voices` to see all the voices.')

#     await ctx.send('Loading...')
#     async with ctx.typing():
#         try:
#             result = await uberduck_client.speak_async(speech, voice, check_every=0.5)
#             file = discord.File(
#                 BytesIO(result),
#                 filename='audio.wav',
#             )
#         except uberduck.UberduckException as e:
#             return await ctx.reply(f'Sorry, an error occured\n{e}')

#         await ctx.send(file=file)

# # @client.slash_command(name='voices',
# #     description='lists the voices you can use',
# #     pass_context=True,
# #     guild_ids=[GUILD_ID],)


# async def voices(ctx):
#     print(ctx)
#     file = discord.File(
#         StringIO(
#             '\n'.join(
#                 await uberduck.get_voices_async(return_only_names=True)
#             )
#         ),
#         filename='voices.txt'
#     )
#     print(file)
#     await ctx.respond(file=file)  # not reply!!!


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
