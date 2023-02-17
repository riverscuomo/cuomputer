from config import GUILD_ID

async def is_message_from_other_guild(message):
    """ Leave the message's guild if it's not yours and returns True. """
    if message.guild is None or message.guild.id != GUILD_ID:
        bad_guild = message.guild

        print(f"wrong guild {bad_guild.name}")
        await bad_guild.leave()
        print(f":ok_hand: Left guild: {bad_guild.name} ({bad_guild.id})")
        return True