from bot.setup.init import client
import sys
from rich import print

sys.path.append("...")  # Adds higher directory to python modules path.
from bot.on_ready.roles_sheet import (
    print_role_ids_to_sheet,
    # print_channel_attributes_to_sheet,
    # set_role_attributes_from_sheet,
)

async def get_last_thousand_messages(guild, thread_id):
    print(f'get_last_thousand_messages {thread_id}')

    thread = await guild.fetch_channel(thread_id)
    # print(thread)

    messages = []
    async for message in thread.history(limit=1000):
        messages.append(message.content)

    return messages

async def fetch_and_print_messages(guild, thread_id):
    messages = await get_last_thousand_messages( guild, thread_id)
    for m in messages:
        print(m)




@client.event
async def on_ready():
    """This runs once (on startup)."""
    print("on_ready")
    # return

    guild = client.get_guild(GUILD_ID)

    # # Run the fetch_and_print_messages function
    # await fetch_and_print_messages(guild, '1098584328335802398')


    channels = await guild.fetch_channels()
    print(channels)

    await print_role_ids_to_sheet()
    # await set_role_attributes_from_sheet()

    # await print_channel_attributes_to_sheet()

    # print("Bot logged in as {0.user} with id {0.user.id}".format(client))
    print("Bot logged in")


from config import GUILD_ID, TOKEN


# import asyncio


# print("in bot.py")

# #


# def main():

#     print("on_ready.main")

#     client.run(TOKEN)


# if __name__ == "__main__":

#     main()
