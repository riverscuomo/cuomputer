from bot.scripts.message.message import (
    append_punctuation,
    # mention,
    # replace_names_with_username,
)
import sys

sys.path.append("...")  # Adds higher directory to python modules path.
# from textblob.blob import TextBlob


def finalize_response(response: str, nick: str, replace_names=False):
    """
    Replace any names with the user's name. Append punctuation.
    """
    # if replace_names:
    #     # response = response + " Dorothy"
    #     response = replace_names_with_username(response, nick)
    # print("after replacing names: ", response)

    # print(language)

    # if language and language != "en":

    #     blob = TextBlob(response)
    #     print(blob)

    #     try:
    #         response = blob.translate(to=language).raw
    #     except Exception as e:
    #         print("Couldn't do blob.translate in finalize_reponse: ", e, blob)

    # print(response)
    response = response.replace("!", ".")

    if not response:
        return ""

    # APPEND PUNCTUATION IF NECESSARY
    response = append_punctuation(response)
    # print(response)

    # # Mention the original poster
    # # 5 in 6 chance
    # # # Unless this is a coaching channel
    # response = mention(nick, response)

    return response
