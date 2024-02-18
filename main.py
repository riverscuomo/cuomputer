# import bot.bot
import asyncio
import bot.on_ready.on_ready
import bot.on_member_join.on_member_join
import bot.on_message.on_message
import bot.on_member_update.on_member_update
from config import TOKEN, GUEST_BOT_TOKEN
from bot.setup.init import client, guest_client
from rich import print
import sys


async def main():
    await asyncio.gather(
        client.start(TOKEN),
        guest_client.start(GUEST_BOT_TOKEN)
    )

if __name__ == '__main__':
    asyncio.run(main())
