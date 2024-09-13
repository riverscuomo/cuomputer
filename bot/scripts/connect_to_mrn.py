# from bot.db.fbdb import db
from bot.db.fbdb import get_firestore_db
import sys

sys.path.append("...")  # Adds higher directory to python modules path.


async def connect_to_mrn(message, member, member_name):
    """
    This asynchronous function connects a user to the riverscuomo.com server using the user's Discord ID.

    Parameters:
    message (Message): It is an object that represents a 'Message' in the context of Discord's communication platform.
    member (Member): It is an object that represents a 'Member' in the context of Discord's Guild(server).
    member_name (str): name or ID of the discord member.

    """

    # Message content is considered as username
    username = message.content

    # If username ends with a dot, the dot is removed
    if username[-1] == ".":
        username = username[:-1]

    db = get_firestore_db()

    # Query the database to get the users having the above username
    users = db.collection("users").where("username", "==", username).get()

    # Check if the username provided does not exist
    if users is [] or users is None or len(users) == 0:
        print("yep")  # Debug print statement
        # Prompt the user to enter the correct username
        await message.channel.send(
            f"There is no neighbor on riverscuomo.com with the username {username}. Make sure you enter your exact riverscuomo.com username, case-sensitive."
        )
        return

    # Select the first user from users list (Assuming no two users have the same username)
    user = users[0]

    # Convert the 'user' document to a dictionary
    data = user.to_dict()

    # Instructions in case discordId is not set in the user's data
    instructions = f"\n\nPlease, go to your profile page at https://riverscuomo.com and enter '{member.id}'. Then come back here and enter your riverscuomo.com username and hit enter."

    # Check if 'discordId' is already set in the user's data
    discord_id = data["discordId"] if "discordId" in data else None

    # If 'discordId' is not set, prompt the user to set it
    if discord_id is None:
        await message.channel.send(
            f"{member_name}, it looks like you haven't entered your discord ID on my website. "
            + instructions
        )
        return

    # Check if 'discordId' is set in the old format (Contains '#')
    if "#" in discord_id:
        await message.channel.send(
            f"{member_name}, the value saved on my website for your discord id is {discord_id}. This might be your short discord ID. We're now using the long discord snowflake ID."
            + instructions
        )
        return

    # Convert discord_id to integer for comparison
    discord_id = int(discord_id)

    # Debug print statements for Discord IDs
    print(discord_id, member.id, discord_id == member.id)
    print(type(discord_id), type(member.id))

    # If the discordId matches with the member's, update discordConnected to True and send a success message
    if discord_id == member.id:
        user.reference.update({"discordConnected": True})
        await message.channel.send(
            f"Riverscuomo.com member '{username}' is now connected to this discord server."
        )
    else:
        # If the discordId does not match, send instruction message
        await message.channel.send(
            f"{member_name}, I found an riverscuomo.com user '{username}' but the value saved on that profile is {discord_id} which does not match your snowflake ID {member.id}. "
            + instructions
        )
    return

# async def connect_to_mrn(message, member, member_name):

#     username = message.content

#     if username[-1] == ".":
#         username = username[:-1]

#     users = db.collection("users").where("username", "==", username).get()

#     if users is [] or users is None or len(users) == 0:
#         print("yep")
#         await message.channel.send(
#             f"There is no neighbor on riverscuomo.com with the username {username}. Make sure you enter your exact riverscuomo.com username, case-sensitive."
#         )
#         return

#     user = users[0]

#     data = user.to_dict()

#     instructions = f"\n\nPlease, go to your profile page at https://riverscuomo.com and enter '{member.id}'. Then come back here and enter your riverscuomo.com username and hit enter."

#     discord_id = data["discordId"] if "discordId" in data else None

#     if discord_id is None:

#         await message.channel.send(
#             f"{member_name}, it looks like you haven't entered your discord ID on my website. "
#             + instructions
#         )
#         return

#     # Handle old discord ids
#     if "#" in discord_id:

#         await message.channel.send(
#             f"{member_name}, the value saved on my website for your discord id is {discord_id}. This might be your short discord ID. We're now using the long discord snowflake ID."
#             + instructions
#         )
#         return

#     discord_id = int(discord_id)

#     print(discord_id, member.id, discord_id == member.id)
#     print(type(discord_id), type(member.id))

#     if discord_id == member.id:
#         user.reference.update({"discordConnected": True})
#         await message.channel.send(
#             f"Riverscuomo.com member '{username}' is now connected to this discord server."
#         )
#     else:

#         await message.channel.send(
#             f"{member_name}, I found an riverscuomo.com user '{username}' but the value saved on that profile is {discord_id} which does not match your snowflake ID {member.id}. "
#             + instructions
#         )
#     return
