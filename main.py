import asyncio
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
