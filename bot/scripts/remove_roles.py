from discord.utils import get
import asyncio
from bot.setup.discord_bot import client
from config import TOKEN, CLIENT_ID


async def remove_all_roles():
    """
    A one-time function to start over with roles.
    Will delete all but the most basic roles.
    """

    safe_roles = ["yes", "Neighbor", "@everyone"]
    print(safe_roles)

    guild = client.fetch_guild(CLIENT_ID)
    print(guild)

    async for member in guild.fetch_members(limit=3000):
        print(member)

        for role in get(member.roles):
            if role.name not in safe_roles:
                await member.remove_roles(role)


def main():
    print("asldkfj")
    client.run(TOKEN)
    asyncio.run(remove_all_roles())


if __name__ == "__main__":
    main()
