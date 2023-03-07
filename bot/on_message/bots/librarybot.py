from datetime import datetime
import random
from rich import print
import re
from bot.db.fetch_data import fetch_entries
from bot.scripts.message.finalize_response import finalize_response  # , firestore_roles
from bot.setup.init import common_words
from config import members_to_skip, always_respond


def build_reply(author_name, entry):

    # print(entry)

    link = entry["link"]
    text = entry["entry"]

    if text.startswith("# "):
        # text = text.split("# ", 1)
        # text = text[1:]
        text = text[2:]

    if entry["entry_length"] > 400:

        reply = text[:400]

    else:
        reply = text

    reply = reply + ".." + link.replace(" ", "%20")

    return reply


def to_alpha_num(s: str):
    """characters not in this regex get removed"""
    return re.sub("[^0-9a-zA-Z']+", "*", s).replace("*", "")


def get_wiki_response(content, pick_random=False):
    """
    Splits the content into words and looks for a Riverpedia entry that has a title or tag that matches one of the words.
    """
    print("get_wiki_response")
    entries = fetch_entries()
    print("entries.length", len(entries))

    if pick_random == True:
        return None
        entry = random.choice(entries)

        while True:
            if recently_used(entry):
                entry = random.choice(entries)
            else:
                return entry

    elements = content.split()
    elements = [to_alpha_num(x).lower() for x in elements if len(x) > 2]
    elements = [x for x in elements if x not in common_words]
    skippers = ["rivers", "cuomo"]
    elements = [x for x in elements if x not in skippers]
    print(elements)

    matching_entries = []

    for e in entries:

        if recently_used(e):

            continue

        for x in elements:
            if x in e["title"].lower() or x in e["tags"]:
                print(
                    f"{x} matches at least one of: '",
                    e["title"].lower(),
                    "' or '",
                    e["tags"],
                )
                matching_entries.append(e)

    if len(matching_entries) > 1:
        # print(matching_entries)
        return random.choice(matching_entries)
    elif len(matching_entries) == 1:
        return matching_entries[0]
    else:
        return None


def recently_used(entry):

    title = entry["title"]

    if "last_used" not in entry:

        return False
    # print(f"'last_used' in {title}")
    now = datetime.now()
    last_used = entry["last_used"]
    delta = now - last_used
    # print(delta)
    minutes = delta.seconds / 60
    # print(minutes)
    if minutes < 240:
        print(f"'{title}' was used {minutes} minutes ago")
        return True


async def post_library_query_response(nick, message, language):
    """
    Any post in any channel that has a string inside of curly braces
    will receive a bot response with the Riverpedia entry, if there is one.
    """
    print("post_library_query_response")
    try:
        query = message.content.split("{")[1].split("}")[0]

        entry = get_wiki_response(query)

        if entry is not None:
            # sleep(t)

            entry["last_used"] = datetime.now()

            reply = build_reply(nick, entry)
            response = finalize_response(reply, language, nick)
            await message.channel.send(response)
            # await message.channel.send(reply)
            return True
    except:
        return


# @client.event
async def post_library_response(nick: str, message, language: str):
    """
    Posts a Riverpedia response if there is one.
    """
    # print("\n")

    # # skip all the processing for simple bots that are just removing posts
    # author_names_to_skip = ["Rivers", "Dyno"]

    # never_respond = 30  # t has to be higher
    # no_river = 80  # if no 'river', t has to be higher
    # no_question = 95  # if no '?', t has to be higher
    # always_respond = 99

    t = random.randint(1, 100)
    content = message.content  # str
    author = message.author  # User
    # author_name = author.name  # Str
    channel = message.channel.name
    # print(t, channel, author, author_name, content)

    # # respond if these conditions are met
    # if (
    #     t > never_respond
    #     and ("?" in content or t > no_question)
    #     and ("river" in content or t > no_river)
    #     and author.id not in members_to_skip
    #     # and channel in bot_response_channels
    # ):

    content = content.lower()

    if t > always_respond:
        entry = get_wiki_response(content, pick_random=True)

        entry["last_used"] = datetime.now()
        reply = build_reply(nick, entry)
        response = finalize_response(reply, language, nick)
        await message.channel.send(response)
        return True

    entry = get_wiki_response(content)

    # while entry is not None == True:
    #     title = entry["title"]
    #     print(f"reject bot response: {title}")
    #     entry = get_wiki_response(content)

    # t = random.randint(2, 5)

    if entry is not None:
        # sleep(t)

        entry["last_used"] = datetime.now()

        reply = build_reply(nick, entry)
        response = finalize_response(reply, language, nick)
        await message.channel.send(response)
        # await message.channel.send(reply)
        return True
    return False


# client.run(TOKEN)
