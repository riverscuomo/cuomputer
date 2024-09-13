import asyncio
from bot.on_ready.on_ready import on_ready
from bot.on_member_join.on_member_join import on_member_join
from bot.on_message.on_message import on_message
from bot.on_member_update.on_member_update import on_member_update
from bot.setup.services.demoji_setup import initialize_demoji
from config import TOKEN
from bot.setup.discord_bot import client


async def main():

    # Initialize demoji for emoji handling
    initialize_demoji()

    await asyncio.gather(
        client.start(TOKEN),
    )

if __name__ == '__main__':
    asyncio.run(main())
