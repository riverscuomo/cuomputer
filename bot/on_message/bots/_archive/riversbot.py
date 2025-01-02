# from bot.setup.resource_manager import resource_manager
# from better_profanity import profanity
# import requests
# import random
# import json
# from bot.scripts.message.finalize_response import finalize_response
# import sys
# # from bot.on_message.bots.gptbot import build_openai_response
# # from bot.scripts.message.message import (
# #     append_punctuation,
# #     mention,
# #     replace_names_with_username,
# # )

# sys.path.append("...")  # Adds higher directory to python modules path.
# # from data.lists import (
# #     questions_and_specific_alerts,
# #     yes_or_no_questions,
# #     yes_or_no_answers,
# #     questions_to_answer_with_random_4,
# # )
# # from flask_login import current_user
# # from textblob import TextBlob
# # from coolname import generate_slug, generate


# async def post_riverbot_response(message):
#     """
#     These are lyrics, movie lines, an inspo quotes.
#     """
#     print("post_riverbot_response()")
#     content = message.content.lower()

#     reply = get_response(content)

#     if reply is None:
#         print("no reply that met condidtions")
#         return

#     while reply is not None and profanity.contains_profanity(reply) == True:
#         print(f"reject bot response: {reply}")
#         reply = get_response(content)

#     response = finalize_response(
#         reply, message.nick, replace_names=True)

#     await message.channel.send(response)

#     return True


# def get_response(message: str):
#     # print("get_response()")

#     # inspiring_lines = get_inspiring_lines()

#     # t = random.randint(1, 100)
#     # # print("t=", t)
#     # print(message)

#     # if (
#     #     ("rivers" in message and t < 20)
#     #     or (("rivers" in message and "?" in message) and t < 80)
#     #     or t < 2
#     # ):

#     #     for q in questions_and_specific_alerts:

#     #         if q[0].lower() in message:
#     #             return q[1]

#     #     for q in questions_to_answer_with_random_4:

#     #         if q.lower() in message:

#     #             return " ".join(generate())

#     #     #  answer common boring questions that don't have articles
#     #     # EITHER / OR
#     #     if " or " in message.lower():
#     #         return random.choice(
#     #             [
#     #                 "the first one.",
#     #                 "the last one.",
#     #                 "either one, I don't care.",
#     #             ]
#     #         )

#     #     for q in yes_or_no_questions:
#     #         if q in message.lower():
#     #             return random.choice(yes_or_no_answers)

#     # if ("rivers" in message and t < 50) or t < 2:

#     t = random.randint(1, 100)
#     # print("t2=", t)

#     # respond with a lyric
#     if t < 33:
#         return random.choice(resource_manager.lyrics)

#     # respond with a movie line.
#     elif t < 66:
#         return random.choice(resource_manager.movie_lines)

#     # last resort: respond with an inspirational quote
#     quote = fetch_quote()

#     return quote.split(" -")[0]

#     # return None


# def fetch_quote():
#     response = requests.get("https://zenquotes.io/api/random")
#     json_data = json.loads(response.text)
#     return json_data[0]["q"] + " -" + json_data[0]["a"]
