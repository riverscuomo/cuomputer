import config as config
from bot.on_message.bots.googlebot import post_google_response
from bot.on_message.bots.qna_default import post_qna_default_response
from bot.on_message.bots.response_handlers import CustomMessage, channels, config, handle_artists_channel, handle_coach_channel, handle_dan_channel, handle_geezerville_channel, handle_language_channels, handle_lounge_channel, handle_movies_tv_books_channel, handle_music_channel, handle_musicians_channel, handle_sarah_channel, handle_zoo_channel, openai_bot
from bot.on_message.bots.rolesbot import post_roles_response
from bot.on_message.classes.message import CustomMessage
from config import channels, bug_report_channels
import time

# dict to store last response time for rctalk
last_response_times = {}

async def respond(message: CustomMessage, channel):
    """ Responds to a message with one of various bots """

    message.log()

    if channel.id in bug_report_channels:
        return

    if await handle_lounge_channel(message, channel):
        return

    if channel.id == channels["qna"]:

        if await post_roles_response(message):
            return

        # if await post_google_response(message):
        #     return

        await post_qna_default_response(message)

    elif await handle_coach_channel(message, channel):
        return #

    elif channel.id == channels["pink"]:
        message.gpt_system = " but you are a gay version of him."
        if (
            (message.is_question and message.mentions_rivers) or
            ((message.is_question or message.mentions_rivers) and message.die_roll > .8) or
            message.mentions_cuomputer or
            (message.die_roll > .99)
        ) and await openai_bot.post_ai_response(message):
            return
        
    elif channel.id == channels["rctalk"]:
        current_time = time.time()
        
        last_response_time = last_response_times.get(channel.id, 0)
        
        if current_time - last_response_time >= 10: # check if cooldown has passed
            await openai_bot.post_ai_response(message)
            last_response_times[channel.id] = current_time # update the last response time for this channel
            return

    elif await handle_sarah_channel(message, channel):
        return
    elif await handle_dan_channel(message, channel):
        return

    elif await handle_geezerville_channel(message, channel):
        return

    elif channel.id == channels["vangie"]:
        message.gpt_system += " - You love to engage in witty banter and have a raunchy sense of humor."
        message.gpt_system += " - Sometimes, as a joke, you can put NSFW text in spoiler tags."
        if message.user_score > config.gpt_threshold and (
            (message.is_question and message.mentions_rivers and message.die_roll > .1) or
            ((message.is_question or message.mentions_rivers) and message.die_roll > .95) or
            message.mentions_cuomputer or
            (message.die_roll > .999)
        ) and await openai_bot.post_ai_response(message):
            return

    elif await handle_artists_channel(message, channel):
        return
    elif await handle_music_channel(message, channel):
        return
    elif await handle_musicians_channel(message, channel):
        return
    elif await handle_movies_tv_books_channel(message, channel):
        return
    elif await handle_zoo_channel(message, channel):
        return
    elif await handle_language_channels(message, channel):
        return

    elif message.die_roll == 97:
        await openai_bot.post_ai_response(message)

    if message.die_roll >= 0.98:
        message.gpt_system = " but actually you are a sarcastic bot who loves to roast people. (all in good fun of course)"

    elif message.is_newbie and message.die_roll > .8:
        await openai_bot.post_ai_response(message)
        return

    elif message.mentions_the_bot_who_is_responding and message.die_roll > .6:
        await openai_bot.post_ai_response(message)
        return
    

