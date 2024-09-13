# from dotenv import load_dotenv
# import os
# from bot.scripts.message.finalize_response import finalize_response
# import requests
# import contextlib
# import sys
# from better_profanity import profanity

# # from bot.on_message.bots.gptbot import build_openai_response, post_ai_response
# # import random
# sys.path.append("...")  # Adds higher directory to python modules path.
# load_dotenv()


# async def post_mongo_response(nick: str, message, language, test_message: str):
#     """
#     These are the mongo db chat history responses. The old bot.
#     """
#     print(f"post_mongo_response for {test_message}")
#     base = os.getenv("CHAT_API")
#     url = base + nick + "/"
#     url = url + test_message
#     response = requests.get(
#         url=url,
#         headers={
#             "TOKEN": os.environ.get("USERS_API_TOKEN"),
#             "userId": os.environ.get("USERS_API_USER_ID")
#         },
#     )

#     # print("post_mongo_response")
#     # print(response.status_code)
#     # print(response.text)
#     # print(response.content)

#     profanity.add_censor_words(["dicks", "racism", "racist", "nuts"])

#     if (
#         response.status_code != 404
#         and "</html>" not in response.text
#         and "@everyone" not in response.text
#         and not profanity.contains_profanity(response.text)
#     ):

#         response = finalize_response(
#             response.text, language, nick, replace_names=True)

#         with contextlib.suppress(Exception):
#             await message.channel.send(response)
#         return True

#     else:
#         print("error getting oldbot response from 1.0/chat/api")
#         return False
