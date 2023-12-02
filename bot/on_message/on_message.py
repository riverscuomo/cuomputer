from bot.on_message.bots.gptbot import post_gpt_response
from datetime import datetime
from rich import print
import random
from bot.on_message.bots.qna_default import post_qna_default_response
from bot.on_message.bots.rolesbot import post_roles_response
from bot.on_message.bots.googlebot import post_google_response
from bot.on_message.bots.librarybot import (
    post_library_query_response,
)
from bot.on_message.bots.knowledgebot import post_google_knowledge_response
from bot.on_message.bots.riversbot import post_riverbot_response
from bot.on_message.bots.mongobot import post_gpt_response
from bot.scripts.add_roles import (
    check_firestore_and_add_roles_and_nick,
    add_time_based_roles,
)
from bot.scripts.message.forbidden import (
    name_contains_profanity,
    message_is_forbidden,
    message_is_too_negative,
)
from bot.scripts.assert_old_users_have_connected import assert_old_users_have_connected
from bot.scripts.delete_message_if_conditions_are_met import (
    reject_artist_text_in_gallery,
    # delete_based_images_in_general,
)
from bot.scripts.is_message_from_another_guild import is_message_from_other_guild
from bot.scripts.is_request_for_server_time import is_request_for_server_time
from bot.scripts.is_request_for_replicate import is_request_for_image
from bot.scripts.message_is_a_skipper import message_is_a_skipper
from rivertils.rivertils import get_test_message_and_language
from bot.scripts.connect_to_mrn import connect_to_mrn
from bot.db.fetch_data import fetch_roles
from bot.setup.init import client, openai_sessions, tz
import config as config
from config import cuomputer_id, channels
import contextlib
import sys
from bot.on_message.classes.message import CustomMessage

# from bot.scripts.message.finalize_response import finalize_response

sys.path.append("...")  # Adds higher directory to python modules path.


# from bot.scripts.is_newbie import is_newbie
# from bot.on_message.bots.flirtybot import post_flirty_response


@client.event
async def on_message(message):
    author = message.author
    channel = message.channel
    now = datetime.now(tz)

    if message_is_a_skipper(message, channel):
        if author.id == cuomputer_id:
            with contextlib.suppress(Exception):
                openai_sessions[channel.name] += f" Rivers Cuomo: {message.content}"
        return

    if await is_message_from_other_guild(message):
        return

    g = message.guild.name  # if message.guild.id != GUILD_ID else ""
    print(f"{g}\"{channel.name}\"<{author.name} {author.id}>:'{message.content}'")

    if await name_contains_profanity(author.name, message):
        return

    roles, role_names = await fetch_roles(message.guild)
    # print(role_names)

    if await message_is_too_negative(message, role_names):
        return

    # 4 represents Friday
    if now.weekday() != 4 and await message_is_forbidden(message, role_names):
        return

    if await is_request_for_server_time(message):
        return

    # Add time-based roles so they can access more channels I MOVED THIS UP
    await add_time_based_roles(author, roles)

    test_message, language_code = get_test_message_and_language(
        message.content)

    if channel.id == channels["connect"] and len(message.content) < 30:
        await connect_to_mrn(message, author, author.name)
        return

    author, nick, firestore_user = await check_firestore_and_add_roles_and_nick(
        author, roles
    )

    # firestore_user["banned"]=True
    # print(firestore_user)
    # print(firestore_user["banned"])
    # print(firestore_user["banned"] == "False")
    # print(firestore_user["banned"] == False)
    if firestore_user is not None and firestore_user["banned"] == True:
        await message.delete()
        return

    if not await assert_old_users_have_connected(message, author, firestore_user):
        return

    # build a list of strings for each of the roles that the author already has
    author_roles = [x.name for x in author.roles]

    # print(now.year, now.month, now.day, now.hour, now.minute, now.second)
    # print(now.hour)

    await reject_artist_text_in_gallery(message, author_roles)
    # await reject_in_focus_channel(message, author_roles)

    # await delete_based_images_in_general(message, author_roles, now)

    # print(firestore_user)
    # await add_remove_roles_for_specific_users(author, roles)

    if await is_request_for_image(message, nick, firestore_user):
        return

    if await post_library_query_response(nick, message, language_code):
        return

    original_message = message

    # from here on out, 'message' refers to the CustomMessage class
    message = CustomMessage(original_message)
    message.message = message
    message.nick = nick
    message.language_code = language_code
    message.test_message = test_message
    message.author_roles = author_roles
    message.firestore_user = firestore_user
    message.user_score = firestore_user["score"]
    message.id_of_user_being_replied_to = await get_user_id(message)
    message.mentions_cuomputer = cuomputer_id in message.raw_mentions or message.id_of_user_being_replied_to == cuomputer_id
    # print(cuomputer_id)
    # print(message.raw_mentions)
    # print(message.id_of_user_being_replied_to)
    # print(cuomputer_id in message.raw_mentions)
    # print(message.mentions_cuomputer)

    print(type(message))

    await respond(message, channel)


async def respond(message: CustomMessage, channel):
    """ Responds to a message with one of various bots """

    message.log()

    if (
            channel.id in [channels["lounge"]]
            and message.user_score > config.gpt_threshold
            and await post_gpt_response(message)):
        return

    # if t==2 and await post_google_knowledge_response(nick, message, language_code):
    #     return

    # if t==3 and await post_google_response(nick, message, language_code):
    #     return

    # if await post_library_response(nick, message, language_code):
    #     return

    # print(channel.id == channels["coach"])
    # print(message.user_score > config.gpt_threshold)
    # print((
    #     (message.is_question and message.mentions_rivers and message.die_roll > .1) or
    #     ((message.is_question or message.mentions_rivers) and message.die_roll > .95) or
    #     message.mentions_cuomputer or
    #     (message.die_roll > .999)
    # ))

    if channel.id == channels["qna"]:

        if await post_roles_response(message):
            return

        if await post_google_knowledge_response(message):
            return

        if await post_google_response(message):
            return

        await post_qna_default_response(message)

    elif channel.id == channels["coach"]:
        if message.user_score > config.gpt_threshold and (
            (message.is_question and message.mentions_rivers and message.die_roll > .1) or
            ((message.is_question or message.mentions_rivers) and message.die_roll > .95) or
            message.mentions_cuomputer or
            (message.die_roll > .999)
        ) and await post_gpt_response(message, system="You are Rivers Cuomo from Weezer and you're a good friend, a good listener, and can serve as a therapist or coach."):
            return

    elif channel.id == channels["dan"]:
        if message.user_score > config.gpt_threshold and (
            (message.is_question and message.mentions_rivers and message.die_roll > .1) or
            ((message.is_question or message.mentions_rivers) and message.die_roll > .95) or
            message.mentions_cuomputer or
            (message.die_roll > .99)
        ) and await post_gpt_response(message, system="you are Rivers Cuomo from Weezer but you have adopted the persona of a hyper-opinionated and knowledgable Weezer fan."):
            return

    elif channel.id == channels["geezerville"]:
        if message.user_score > config.gpt_threshold and (
            (message.is_question and message.mentions_rivers and message.die_roll > .1) or
            ((message.is_question or message.mentions_rivers) and message.die_roll > .95) or
            message.mentions_cuomputer or
            (message.die_roll > .999)
        ) and await post_gpt_response(message, system="you are Rivers Cuomo from Weezer. But you're not trying to act younger than you are (53). You're okay talking about middle-age issues including having kids. You sometimes reference 80's nostalgia. ", adjective="nostalgic and sweet"):
            return

    elif channel.id == channels["pink"]:
        if (
            (message.is_question and message.mentions_rivers) or
            ((message.is_question or message.mentions_rivers) and message.die_roll > .8) or
            message.mentions_cuomputer or
            (message.die_roll > .99)
        ) and await post_gpt_response(message, system="You are a gay version of Rivers Cuomo from Weezer."):
            return

    elif channel.id == channels["vangie"]:
        if message.user_score > config.gpt_threshold and (
            (message.is_question and message.mentions_rivers and message.die_roll > .1) or
            ((message.is_question or message.mentions_rivers) and message.die_roll > .95) or
            message.mentions_cuomputer or
            (message.die_roll > .999)
        ) and await post_gpt_response(message, system="You are Rivers Cuomo from Weezer but are very smart and smooth and like to flirt with women in a way they enjoy."):
            return

    elif channel.id in [channels["korean"], channels["japanese"]]:
        if (
            (message.is_question and message.mentions_rivers) or
            ((message.is_question) and message.die_roll > .5) or
            ((message.mentions_rivers) and message.die_roll > .5) or
            message.mentions_cuomputer or
            (message.die_roll > .6)
        ) and await post_gpt_response(message):
            return

    elif message.is_newbie and message.die_roll > .94:
        await post_gpt_response(message)
        return

    elif message.die_roll > .99:
        await post_gpt_response(message)


async def get_user_id(message):
    id_of_user_being_replied_to = None
    if message.reference:
        message_being_replied_to = await client.get_channel(message.reference.channel_id).fetch_message(message.reference.message_id)
        id_of_user_being_replied_to = message_being_replied_to.author.id
    return id_of_user_being_replied_to


# async def post_qna_default_response(nick, message, language_code):

#     response = "I'm sorry, I don't understand. This channel is for questions related to the operation of my server."
#     response = finalize_response(response, language_code, nick)
#     response += "\n\n"

#     reply = [
#         response,
#         "To have a fun conversation with me: please use the #coach-cuomo channel--but make sure you have the Neighbor role first.\n",
#         "To report a bug: please use the relevant channel in the Tech Support section.\n",
#     ]
#     # response = finalize_response(reply, language_code, nick)
#     await channel.send("".join(reply))
