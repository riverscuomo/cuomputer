from deprecated import deprecated


def get_firestore_user(discord_id, firestore_users):
    """
    Iterate through the mrn user objects
    and compare to the discord id of the member who sent
    this message.

    These are loaded when you run the bot.
    """
    # print(discord_id)

    for user in firestore_users:

        if type(discord_id) == str and "#" in discord_id:
            return None

        try:
            if int(discord_id) == int(user["discordId"]):
                return user
        except:
            print(f'get_firestore_user failed for {discord_id} or {user["discordId"]}')
