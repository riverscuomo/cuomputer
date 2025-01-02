from bot.on_message.bots.openai_bot import OpenAIBot
from bot.on_message.bots.weezerpedia import WeezerpediaAPI
from bot.on_message.bots.riverpedia_api import RiverpediaAPI
from config import long_name, short_name

riverpedia_api = RiverpediaAPI()
weezerpedia_api = WeezerpediaAPI()

# Instantiate OpenAIBot
openai_bot = OpenAIBot(
    long_name=long_name,
    short_name=short_name,
    weezerpedia_api=weezerpedia_api
)
