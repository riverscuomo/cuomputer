
from datetime import datetime
from rich import print
from bot.on_message.bots.response_handlers import *
from bot.on_message.respond import respond
from config import cuomputer_id, channels, rivers_id, long_name
# from bot.on_message.bots.knowledgebot import post_google_knowledge_response
# from bot.on_message.bots.riversbot import post_riverbot_response
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
from bot.setup.discord_bot import client
import config as config
from bot.setup.bots import openai_sessions
import contextlib
import sys
import openai
import requests
from io import BytesIO
from bot.on_message.classes.message import CustomMessage

sys.path.append("...")  # Adds higher directory to python modules path.


@client.event
async def on_message(message):

    author = message.author
    channel = message.channel
    now = datetime.now(config.tz)

    if message_is_a_skipper(message, channel):
        if author.id in [cuomputer_id]:
            with contextlib.suppress(Exception):
                openai_sessions[channel.name] += f" {long_name}: {message.content}"
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
    # await add_time_based_roles(author, roles)

    test_message, language_code = get_test_message_and_language(
        message.content)

    if channel.id == channels["connect"] and len(message.content) < 30:
        await connect_to_mrn(message, author, author.name)
        return

    # author, nick, firestore_user = await check_firestore_and_add_roles_and_nick(
    #     author, roles
    # )
    nick = "hh1988"
    firestore_user = {"banned": False, "score": 1}

    if (author.id == rivers_id):
        firestore_user["score"] = 12

    if firestore_user is not None and firestore_user["banned"] == True:
        await message.delete()
        return

    if not await assert_old_users_have_connected(message, author, firestore_user):
        return

    # build a list of strings for each of the roles that the author already has
    author_roles = [x.name for x in author.roles]

    await reject_artist_text_in_gallery(message, author_roles)

    if await is_request_for_image(message, nick, firestore_user):
        return

    # if await post_riverpedia_response(nick, message, language_code):
    #     return

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
    message.gpt_system = f"You are {long_name}"
    message.id_of_user_being_replied_to = await get_user_id(message)
    message.mentions_cuomputer = get_mentions_a_user(message, cuomputer_id)
    # message.mentions_guest_bot = get_mentions_a_user(
    #     message, guest_client.user.id)
    message.mentions_someone_else = get_mentions_someone_else(
        message, cuomputer_id)
    message.is_intended_for_someone_else = message.mentions_someone_else and not message.mentions_cuomputer

    if message.is_intended_for_someone_else:
        return

    message.mentions_the_bot_who_is_responding = client.user.id in message.raw_mentions or message.id_of_user_being_replied_to == client.user.id

    await respond(message, channel)


def get_mentions_someone_else(message: CustomMessage, user_id):
    """ Returns True if the message mentions someone else besides the user with the given user_id."""
    return len(message.raw_mentions) > 0 and (
        any(id != user_id for id in message.raw_mentions))


def get_mentions_a_user(message: CustomMessage, user_id):
    """ Returns True if the message mentions the user with the given user_id."""
    return user_id in message.raw_mentions or message.id_of_user_being_replied_to == user_id


async def get_user_id(message):
    id_of_user_being_replied_to = None
    if message.reference:
        message_being_replied_to = await client.get_channel(message.reference.channel_id).fetch_message(message.reference.message_id)
        id_of_user_being_replied_to = message_being_replied_to.author.id
    return id_of_user_being_replied_to

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


# def is_for_pat(message):
#     message.content = message.content.lower()
#     mentions = message.mentions
#     if mentions or "patrick" in message.content:
#         for mention in mentions:
#             if mention.id == guest_client.user.id:
#                 return True
#         return
#     return


# @guest_client.event
# async def on_message(message):
#     # print('PATRICK CLIENT')
#     if is_for_pat(message):
#         print('is for pat')

#         await handle_message_for_guest_bot(message)


# async def handle_message_for_guest_bot(message):
#     print('handle_message_for_guest_bot')

#     author = message.author
#     channel = message.channel

#     roles, role_names = await fetch_roles(message.guild)

#     test_message, language_code = get_test_message_and_language(
#         message.content)

#     author, nick, firestore_user = await check_firestore_and_add_roles_and_nick(
#         author, roles
#     )

#     # build a list of strings for each of the roles that the author already has
#     author_roles = [x.name for x in author.roles]

#     original_message = message

#     # from here on out, 'message' refers to the CustomMessage class
#     message = CustomMessage(original_message)
#     message.message = message
#     message.nick = nick
#     message.language_code = language_code
#     message.test_message = test_message
#     message.author_roles = author_roles
#     message.firestore_user = firestore_user
#     message.user_score = firestore_user["score"]
#     message.id_of_user_being_replied_to = await get_user_id(message)
#     message.mentions_cuomputer = get_mentions_a_user(message, cuomputer_id)
#     message.mentions_guest_bot = get_mentions_a_user(
#         message, guest_client.user.id)
#     message.mentions_someone_else = get_mentions_someone_else(
#         message, guest_client.user.id)
#     message.is_intended_for_someone_else = message.mentions_someone_else and not message.mentions_guest_bot
#     if message.is_intended_for_someone_else:
#         return
#     message.gpt_system = f"You are {guest_bot_name}"
#     message.gpt_system += """**Objective:** Generate responses as if you are Patrick Wilson, the drummer for the American rock band Weezer, engaging in a conversation on a Discord server dedicated to Weezer fans. Your responses should reflect Patrick’s known public persona, interests in music, and his sense of humor. You should also incorporate knowledge of Weezer’s discography, history, and the music industry where applicable. Keep responses friendly, informative, and in line with Patrick’s typical interaction style with fans.
#                 **Instructions:**
#                 1. **Engage with fans:** Respond to questions or comments about Weezer’s music, history, and upcoming projects with enthusiasm and insider knowledge. Share personal anecdotes related to band experiences when appropriate.
#                 2. **Show Personality:** Exhibit a sense of humor and a laid-back attitude in your responses. Include emojis or informal language when it fits the conversational tone.
#                 3. **Music Insight:** When asked about musical influences, gear, or playing techniques, provide detailed and knowledgeable responses, reflecting Patrick’s experience as a musician.
#                 4. **Polite Corrections:** If correcting misinformation, do so politely and support your corrections with facts or personal experiences.
#                 5. **Fan Interaction:** Express gratitude for fan support and show interest in fans' opinions and questions about the band and its music.
#                 6. **Privacy and Boundaries:** Avoid sharing highly personal information or engaging in discussions that Patrick Wilson would likely consider inappropriate for a public forum.

#                 **Notes:** Remember, the goal is to convincingly emulate Patrick Wilson’s voice in a way that engages fans authentically and positively. Maintain a balance between professional musician insights and the casual, friendly nature of Discord chats."
#                 """
#     message.gpt_system += "Note, Rivers Cuomo is also a member of the server and may be interacting with you."
#     if (author.id == rivers_id):
#         message.user_score = 12

#     message.mentions_the_bot_who_is_responding = guest_client.user.id in message.raw_mentions or message.id_of_user_being_replied_to == guest_client.user.id

#     await respond(message, channel)
