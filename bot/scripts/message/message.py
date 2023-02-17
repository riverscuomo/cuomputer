import sys

sys.path.append("...")  # Adds higher directory to python modules path.
from bot.setup.init import names
from data.lists import *
from rivertils.lists import *
import random
import re
import string
from coolname import generate_slug, generate
# from flask_login import current_user, login_required


def get_language(test_message):
    language = None
    if len(test_message) < 3:
        language = "en"
    else:
        # phrases like 'haha' are triggering bizarre language ids
        for x in indicates_english_message:
            if x.lower() in test_message.lower():
                language = "en"
    return language


def cleaned(word):
    word = word.replace(".", "")
    word = word.replace("'s", "")
    word = word.replace('"', "")
    # word = word.replace("*", "")
    # print(word)
    return word


def remove_substring_case_insensitive(message):

    # print(message)

    for x in strings_to_delete_case_insensitive:

        pattern = re.compile(x, re.IGNORECASE)
        message = pattern.sub("", message).strip()
    # print(message)
    return message



def mention(nick: str, message: str):
    """
    Mention the original poster.
    and the lowercase the first letter of the message unless it is an 'I'

    """
    # t = random.randint(1, 6)
    t = 1
    if t < 6:
        # print(list(message))
        # print("to lower", message[0])
        # print(message[:2])
        if message[:2] != "I " and message[:2] != "I'":

            message = message[0].lower() + message[1:]
        return nick.capitalize() + ", " + message
    else:
        return message


def mentions_rivers(message):
    if (
        ("rivers" in message.lower())
        or ("cuomo" in message.lower())
        or ("リバース" in message)
    ):
        return True
    else:
        return False



def replace_names_with_username(message: str, nick: str):

    # names = get_names()

    # Split the repsonse into a list of individual words
    words = message.split()
    # print(words)

    name_to_replace = None
    names_found = 0

    for word in words:

        # if name_to_replace is None:

        # Take off apostrophe s
        word = word.split("'")[0]
        # print(word.strip())

        # Remove any punctuation on the word
        word = word.translate(str.maketrans("", "", string.punctuation))

        # don't use lower becuase of names that are also common words, like charity, hope
        if word.strip() in names:

            names_found += 1

            if names_found > 1:
                name_to_replace = word.strip()
                # print(name_to_replace)

                # break

    if name_to_replace:
        # replace all the occurences of just that one name with the user's name
        # message = message.replace(name_to_replace, current_user.username.title())
        message = message.replace(name_to_replace, nick)

    return message



def is_question(string):
    questions = ["who", "what", "when", "where", "why", "how"]
    for x in questions:
        if x in string.lower():
            return True
    return False


def append_punctuation(string):

    if re.match(r"[a-zA-Z0-9]", string[-1]):
        if is_question(string):
            return string + "?"
        else:
            return string + "."
    return string
