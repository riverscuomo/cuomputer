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
from bot.scripts.connect_to_mrn import connect_to_mrn
from bot.db.fetch_data import fetch_roles
from bot.setup.discord_bot import client
import config as config
import contextlib
import sys
from bot.on_message.classes.message import CustomMessage

sys.path.append("...")  # Adds higher directory to python modules path.


@client.event
async def on_message(message):
    """
    Processes all messages sent in the Discord server.
    
    This function handles the core message processing logic, including
    the Discord-Weezify connection flow:
    
    Discord-Weezify Connection Related Tasks:
    1. When a message is sent in the #connect-to-mrn channel:
       - Calls connect_to_mrn() to process the connection request
       - This is where users send their Weezify username to connect accounts
    
    2. For messages in other channels:
       - Checks if the user has a connected Weezify account via assert_old_users_have_connected()
       - If not connected, deletes the message and sends connection instructions
    
    The connection flow is:
    1. User receives snowflake ID from on_member_join
    2. User enters ID on Weezify profile
    3. User sends username in #connect-to-mrn channel (handled here)
    4. Bot verifies and completes connection
    
    Parameters:
    message (Message): The Discord message object
    
    Returns:
    None
    """

    author = message.author
    channel = message.channel
    now = datetime.now(config.tz)

    if message_is_a_skipper(message, channel):
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
    
    # If the message contains a link, delete it
    if message.content.startswith("https://") or message.content.startswith("http://"):
        await message.delete()

    # 4 represents Friday
    if now.weekday() != 4 and await message_is_forbidden(message, role_names):
        return

    if await is_request_for_server_time(message):
        return

    # Add time-based roles so they can access more channels I MOVED THIS UP
    await add_time_based_roles(author, roles)

    test_message = message.content
    
    if channel.id == channels["connect"] and len(message.content) < 30:
        # This is where the Discord-Weezify connection happens when a user types
        # their Weezify username in the connect channel
        await connect_to_mrn(message, author, author.name)
        return

    author, nick, firestore_user = await check_firestore_and_add_roles_and_nick(
        author, roles
    )

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

    original_message = message

    # from here on out, 'message' refers to the CustomMessage class
    message = CustomMessage(original_message)
    message.message = message
    message.nick = nick
    message.test_message = test_message
    message.author_roles = author_roles
    message.firestore_user = firestore_user
    
    # The standardize_firestore_user function ensures "score" exists, so we can use it directly
    message.user_score = firestore_user["score"] if firestore_user else 0
        
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
