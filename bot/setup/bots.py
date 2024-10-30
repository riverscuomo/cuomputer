from bot.on_message.bots.openai_bot import OpenAIBot
from bot.on_message.bots.weezerpedia import WeezerpediaAPI
from bot.on_message.bots.riverpedia_api import RiverpediaAPI
from bot.setup.services.openai_sessions import init_openai_sessions
from config import long_name, short_name

# Initialize any required sessions (like OpenAI sessions)
openai_sessions = init_openai_sessions()


# riverpedia_api = RiverpediaAPI()
weezerpedia_api = WeezerpediaAPI()

# Instantiate OpenAIBot
openai_bot = OpenAIBot(
    long_name=long_name,
    short_name=short_name,
    openai_sessions=openai_sessions,
    weezerpedia_api=weezerpedia_api
)
