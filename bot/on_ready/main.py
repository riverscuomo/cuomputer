""" 
Import this file from the top package level and it will run independently.
I'm currently running it from a file called runner.py.

I think there's a rate-limiting issue with the discord API???
"""
from config import GUILD_ID, TOKEN
from bot.setup.discord_bot import client
from rich import print
import sys

sys.path.append("...")  # Adds higher directory to python modules path.
print(sys.path)


print("in bot.on_ready.main")


client.run(TOKEN)
