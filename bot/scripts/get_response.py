# import sys

# sys.path.append("...")  # Adds higher directory to python modules path.
# from bot.scripts.message.message import remove_at
# from rivertils.lists import indicates_english_message
# from rivertils.rivertils import get_language
# from textblob import TextBlob


# # def get_test_message_and_language(message: str):
# #     """
# #     Removes any @mention at the start of the message string.
# #     If the message is not english, it translates it to english.
# #     Also, returns a language code to let you know which language the user is communicating in.
# #     """
# #     # print("get_test_message_and_language()")

# #     # response = None
# #     language = None

# #     test_message = remove_at(message)
# #     # print(test_message)

# #     blob = TextBlob(test_message)
# #     # print(blob)

# #     language = get_language(test_message)
# #     # print(language)

# #     if not language:

# #         try:
# #             # Get the language of the message

# #             language = blob.detect_language()
# #             # print(language)
# #         except Exception as e:
# #             # print(
# #             #     "Couldn't do blob.detect_language in get_response.py: ",
# #             #     e,
# #             #     blob,
# #             #     language,
# #             # )
# #             language = "en"

# #     if language and language != "en":
# #         try:
# #             test_message = blob.translate(from_lang=language, to="en")
# #             test_message = test_message.raw
# #         except Exception as e:
# #             print("Couldn't do blob.translate in get_response: ", e, blob, language)
# #     # print(message)

# #     # response = get_chatterbot(test_message)

# #     # print(test_message, language)
# #     return test_message, language
# #     # return response


# # def get_language(test_message):
# #     """
# #     A crude quick test likely returns None
# #     """
# #     language = None
# #     if len(test_message) < 3:
# #         language = "en"
# #     else:
# #         # phrases like 'haha' are triggering bizarre language ids
# #         for x in indicates_english_message:
# #             if x.lower() in test_message.lower():
# #                 language = "en"
# #     return language
