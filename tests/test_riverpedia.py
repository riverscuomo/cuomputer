
# Testing the RiverpediaAPI class
from bot.on_message.bots.riverpedia_api import RiverpediaAPI


def test_riverpedia():
    api = RiverpediaAPI()
    content = "frank cuomo"
    response = api.get_wiki_response(content)
    print(response)


if __name__ == "__main__":
    test_riverpedia()
