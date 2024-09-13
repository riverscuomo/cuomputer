from bot.on_message.bots.openai_bot import OpenAIBot
from bot.on_message.bots.weezerpedia import WeezerpediaAPI  # if you need it
from bot.setup.services.openai_sessions import init_openai_sessions
from config import long_name, short_name
from bot.setup.services.file_loader import get_lines_from_file

# Initialize any required sessions (like OpenAI sessions)
openai_sessions = init_openai_sessions()

# Initialize WeezerpediaAPI if needed
weezerpedia_api = WeezerpediaAPI()

# Instantiate OpenAIBot
openai_bot = OpenAIBot(
    long_name=long_name,
    short_name=short_name,
    openai_sessions=openai_sessions,
    weezerpedia_api=weezerpedia_api
)


class ResourceManager:
    def __init__(self):
        self.common_words = get_lines_from_file("common_words")
        self.lyrics = get_lines_from_file("lyrics rc 13 plus chars")
        self.movie_lines = get_lines_from_file("formatted_movie_lines")
        self.pickup_lines = get_lines_from_file("pickup_lines")
        self.inspiring = get_lines_from_file("inspiring")
        self.sweet_things = get_lines_from_file("sweet_things")
        boy_names = get_lines_from_file("boy_names")
        girl_names = get_lines_from_file("girl_names")
        self.names = [x.title() for x in boy_names + girl_names]


# Instantiate ResourceManager
resource_manager = ResourceManager()
