from rich import print
import sys

sys.path.append("...")  # Adds higher directory to python modules path.
print(sys.path)
from bot.setup.init import client

from config import TOKEN

import bot.on_member_update.on_member_update
import bot.on_message.on_message
import bot.on_member_join.on_member_join
import bot.on_ready.on_ready

print("in bot.py")

client.run(TOKEN)
