from bot.on_message.bots.weezerpedia import WeezerpediaAPI


def test():
    # Create an instance of the WeezerpediaAPI class
    # wiki_api = WeezerpediaAPI()

    # # Call the methods to fetch page information and content
    # wiki_api.fetch_page_info()
    # wiki_api.fetch_page_content()

    api = WeezerpediaAPI()
    knowledge, img = api.get_search_result_knowledge(
        "bokkus", False)
    print(knowledge)


if __name__ == "__main__":
    test()
