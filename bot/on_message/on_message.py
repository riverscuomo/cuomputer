import contextlib
import sys

from bot.scripts.message.finalize_response import finalize_response

sys.path.append("...")  # Adds higher directory to python modules path.

from config import cuomputer_id, channels
import config as config


from bot.setup.init import client, openai_sessions
from bot.db.fetch_data import fetch_roles
from bot.scripts.connect_to_mrn import connect_to_mrn
from rivertils.rivertils import get_test_message_and_language
from bot.scripts.message_is_a_skipper import message_is_a_skipper
from bot.scripts.is_request_for_replicate import is_request_for_replicate_image
from bot.scripts.is_request_for_server_time import is_request_for_server_time
from bot.scripts.is_message_from_another_guild import is_message_from_other_guild
from bot.scripts.delete_message_if_conditions_are_met import (
    reject_artist_text_in_gallery,
    delete_based_images_in_general,
)
from bot.scripts.is_newbie import is_newbie
from bot.scripts.assert_old_users_have_connected import assert_old_users_have_connected
from bot.scripts.message.forbidden import (
    name_contains_profanity,
    message_is_forbidden,
    message_is_too_negative,
)
from bot.scripts.add_roles import (
    check_firestore_and_add_roles_and_nick,
    add_time_based_roles,
)
from bot.on_message.bots.mongobot import post_gpt_response
from bot.on_message.bots.riversbot import post_riverbot_response
from bot.on_message.bots.knowledgebot import post_google_knowledge_response
from bot.on_message.bots.librarybot import (
    post_library_query_response,
)
from bot.on_message.bots.flirtybot import post_flirty_response
from bot.on_message.bots.googlebot import post_google_response
from bot.on_message.bots.rolesbot import post_roles_response
from bot.on_message.bots.qna_default import post_qna_default_response

import random
from rich import print
from datetime import datetime, timezone, timedelta
import pytz
from bot.on_message.bots.gptbot import post_gpt_response
tz = pytz.timezone('America/Los_Angeles')

@client.event
async def on_message(message):

    author = message.author
    channel = message.channel

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

    if await message_is_forbidden(message, role_names):
        return

    if await is_request_for_server_time(message, author):
        return    

    # Add time-based roles so they can access more channels I MOVED THIS UP
    await add_time_based_roles(author, roles)

    test_message, language_code = get_test_message_and_language(message.content)   

    if channel.id == channels["connect"] and len(message.content) < 30:
        await connect_to_mrn(message, author, author.name)
        return

    author, nick, firestore_user = await check_firestore_and_add_roles_and_nick(
        author, roles
    )

    await assert_old_users_have_connected(message, author, firestore_user)

    # build a list of strings for each of the roles that the author already has
    author_roles = [x.name for x in author.roles]

    now = datetime.now(tz)
    # print(now.year, now.month, now.day, now.hour, now.minute, now.second)
    # print(now.hour)

    await reject_artist_text_in_gallery(message, author_roles)
    # await reject_in_focus_channel(message, author_roles)

    await delete_based_images_in_general(message, author_roles, now)

    # print(firestore_user)
    # await add_remove_roles_for_specific_users(author, roles)

    if await is_request_for_replicate_image(message, author_roles, firestore_user):
        return


    if await post_library_query_response(nick, message, language_code):
        return


    await respond(nick, message, language_code, test_message, author, channel, author_roles, firestore_user)


async def respond(nick, message, language_code, test_message, author, channel, author_roles, firestore_user):
    """ Responds to a message with one of various bots """

    # a variable which holds a random float between 0 and 1
    t = random.random()
    id_of_user_being_replied_to = await get_user_id(message)
    is_newbie = datetime.now(tz) - author.joined_at  < timedelta(days= 7)
    is_question = message.content[-1]=='?'
    mentions_rivers = 'rivers' in message.content.lower() # i think testmessage doesn't have 'rivers' in it
    mentions_cuomputer  = cuomputer_id in message.raw_mentions or id_of_user_being_replied_to == cuomputer_id
    user_score = firestore_user["score"]
    print(f"t={ round(t, 3)} user_score={user_score}, language_code={language_code}, is_newbie={is_newbie}, is_question={is_question}, mentions_rivers={mentions_rivers}, mentions_cuomputer={mentions_cuomputer}")

    # if meets_conditions_for_standard_response(t, message, newbie):
    #     print("meets conditions for standard response")


    if (
        channel.id in [channels["lounge"]]
        and user_score > config.gpt_threshold
        and await post_gpt_response(
            nick, message, language_code, test_message
        )
    ):
        return

    # if t==2 and await post_google_knowledge_response(nick, message, language_code):
    #     return

    # if t==3 and await post_google_response(nick, message, language_code):
    #     return

    # if await post_library_response(nick, message, language_code):
    #     return



    if channel.id == channels["qna"]:

        if await post_roles_response(nick, message, language_code, test_message):
            return

        if await post_google_knowledge_response(nick, message, language_code):
            return

        if await post_google_response(nick, message, language_code):
            return

        await post_qna_default_response(nick, message, language_code)

    elif channel.id in [channels["coach"], channels["vangie"], channels["dan"]]:
        if channel.id == channels["vangie"]:
            adjective = "funny and flirtatious"
        else: 
            adjective = "funny"
        if user_score > config.gpt_threshold and  (
            (is_question and mentions_rivers and t > .1) or 
            ((is_question or mentions_rivers) and t > .95) or
            mentions_cuomputer or
             (t >.999)
        ) and await post_gpt_response(nick, message, language_code, adjective=adjective):
            return

    elif channel.id == channels["vangie"]:
        if (
            (is_question and mentions_rivers and t > .1) or 
            ((is_question or mentions_rivers) and t > .95) or
            mentions_cuomputer or
             (t >.999)
        ) and await post_gpt_response(nick, message, language_code, adjective="funny"):
            return

    elif channel.id == channels["pink"]:
        if (
            (is_question and mentions_rivers ) or 
            ((is_question or mentions_rivers) and t > .8) or
             mentions_cuomputer or
             (t >.99)
        ) and await post_gpt_response(nick, message, language_code, adjective="flamboyant"):
            return

    elif message.channel.id in [channels["korean"], channels["japanese"] ]:
        if (
        (is_question and mentions_rivers) or 
        ((is_question) and t > .5) or
        ((mentions_rivers) and t > .5) or
         mentions_cuomputer or
            (t >.6)
        ) and await post_gpt_response(nick, message, language_code):
            return

    elif is_newbie and t >.96:
        await post_gpt_response(nick, message, language_code)
        return

    # # could make these conditions explicit
    # elif 
    #     return

    elif t>.997:
        await post_riverbot_response(nick, message, language_code)

async def get_user_id(message):
    id_of_user_being_replied_to = None
    if message.reference:
        message_being_replied_to= await client.get_channel(message.reference.channel_id).fetch_message(message.reference.message_id)
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
#     await message.channel.send("".join(reply))



