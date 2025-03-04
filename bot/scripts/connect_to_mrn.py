from bot.db.fbdb import get_firestore_db
import sys

sys.path.append("...")  # Adds higher directory to python modules path.


async def connect_to_mrn(message, member, member_name):
    """
    Connects a Discord user to their Weezify account.
    
    This function processes messages in the #connect-to-mrn channel and verifies the connection
    between a Discord user and their Weezify account. The connection process works as follows:
    
    Connection Process:
    1. User creates a Weezify account at https://www.weezify.web.app
    2. User goes to their profile screen on the Weezify site
    3. User enters their Discord snowflake ID on their Weezify profile
    4. User sends a message in the #connect-to-mrn channel containing only their Weezify username
    5. This function verifies the Discord ID matches what's in the database
    6. If verified, the user gets a confirmation message and their discordConnected flag is set to True
    
    User Instructions (pinned in #connect-to-mrn channel):
    ```
    1. Make sure you have created a Weezify account at https://www.weezify.web.app
    2. Go to your profile screen at https://www.weezify.web.app
    3. Enter your discord snowflake id*
    4. Come back to this channel
    5. Send a message that consists only of your MRN username (case-sensitive)
    6. The bot will reply with a message confirming connection
    
    *HOW TO FIND YOUR DISCORD SNOWFLAKE ID: 
    First, try typing your MRN username (case-sensitive) in this channel. The bot will reply with your discord snowflake ID.
    OR
    In any Discord server, click the Users icon in the upper right corner. Find your username in the list of users, 
    right click it, and then select Copy ID.
    ```
    
    Known Issues:
    - DM Privacy: Users with restrictive DM settings won't receive the snowflake ID message
    - Channel Permissions: Some roles may need explicit permissions to see the channel
    
    Parameters:
    message (Message): A Discord message object from the connect channel
    member (Member): The Discord member object of the user attempting to connect
    member_name (str): Name or ID of the Discord member
    
    Returns:
    None
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
        print("connect_to_mrn: yep")  # Debug print statement
        # Prompt the user to enter the correct username
        await message.channel.send(
            f"There is no neighbor on Weezify with the username {username}. Make sure you enter your exact Weezify username, case-sensitive."
        )
        return

    # Select the first user from users list (Assuming no two users have the same username)
    user = users[0]

    # Convert the 'user' document to a dictionary
    data = user.to_dict()

    # Instructions in case discordId is not set in the user's data
    instructions = f"\n\nPlease, go to your profile page at https://weezify.web.app and enter '{member.id}'. Then come back here and enter your Weezify username and hit enter."

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

    # Debug print statements for Discord IDs - now with better descriptive labels
    print(f"connect_to_mrn: User '{username}' - Firestore discord_id ID: {discord_id}, Discord discord ID: {member.id}, Match: {discord_id == member.id}")
    # print(type(discord_id), type(member.id))

    # If the discordId matches with the member's, update discordConnected to True and send a success message
    if discord_id == member.id:
        user.reference.update({"discordConnected": True})
        await message.channel.send(
            f"Weezify member '{username}' is now connected to this discord server."
        )
    else:
        # If the discordId does not match, send instruction message
        await message.channel.send(
            f"{member_name}, I found a Weezify user '{username}' but the value saved on that profile is {discord_id} which does not match your snowflake ID {member.id}. "
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
#             f"There is no neighbor on Weezify with the username {username}. Make sure you enter your exact Weezify username, case-sensitive."
#         )
#         return

#     user = users[0]

#     data = user.to_dict()

#     instructions = f"\n\nPlease, go to your profile page at https://weezify.web.app and enter '{member.id}'. Then come back here and enter your Weezify username and hit enter."

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
#             f"Weezify member '{username}' is now connected to this discord server."
#         )
#     else:

#         await message.channel.send(
#             f"{member_name}, I found a Weezify user '{username}' but the value saved on that profile is {discord_id} which does not match your snowflake ID {member.id}. "
#             + instructions
#         )
#     return
