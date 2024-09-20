from bot.setup.services.file_loader import get_lines_from_file


class ResourceManager:
    def __init__(self):
        self.common_words = get_lines_from_file("common_words")
        # self.lyrics = get_lines_from_file("lyrics rc 13 plus chars")
        # self.movie_lines = get_lines_from_file("formatted_movie_lines")
        # self.pickup_lines = get_lines_from_file("pickup_lines")
        # self.inspiring = get_lines_from_file("inspiring")
        # self.sweet_things = get_lines_from_file("sweet_things")
        boy_names = get_lines_from_file("boy_names")
        girl_names = get_lines_from_file("girl_names")
        self.names = [x.title() for x in boy_names + girl_names]


# Instantiate ResourceManager
resource_manager = ResourceManager()
