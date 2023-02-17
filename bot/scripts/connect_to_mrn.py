import sys

sys.path.append("...")  # Adds higher directory to python modules path.

from bot.db.fbdb import db


async def connect_to_mrn(message, member, member_name):

    username = message.content

    if username[-1] == ".":
        username = username[:-1]

    users = db.collection("users").where("username", "==", username).get()

    if users is [] or users is None or len(users) == 0:
        print("yep")
        await message.channel.send(
            f"There is no neighbor on riverscuomo.com with the username {username}. Make sure you enter your exact riverscuomo.com username, case-sensitive."
        )
        return

    user = users[0]

    data = user.to_dict()

    instructions = f"\n\nPlease, go to your profile page at https://riverscuomo.com and enter '{member.id}'. Then come back here and enter your riverscuomo.com username and hit enter."

    discord_id = data["discordId"] if "discordId" in data else None

    if discord_id is None:

        await message.channel.send(
            f"{member_name}, it looks like you haven't entered your discord ID on my website. "
            + instructions
        )
        return

    # Handle old discord ids
    if "#" in discord_id:

        await message.channel.send(
            # f"{member_name}, it looks like you haven't updated your discord ID on MRN to your  "
            f"{member_name}, the value saved on my website for your discord id is {discord_id}. This might be your short discord ID. We're now using the long discord snowflake ID."
            + instructions
        )
        return

    discord_id = int(discord_id)

    print(discord_id, member.id, discord_id == member.id)
    print(type(discord_id), type(member.id))
    # print(discord_id - member.id)

    if discord_id == member.id:
        user.reference.update({"discordConnected": True})
        await message.channel.send(
            f"Riverscuomo.com member '{username}' is now connected to this discord server."
        )
    else:
        
        await message.channel.send(
            f"{member_name}, I found an riverscuomo.com user '{username}' but the value saved on that profile is {discord_id} which does not match your snowflake ID {member.id}. "
            + instructions
        )
    return
