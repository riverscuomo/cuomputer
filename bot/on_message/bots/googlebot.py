from config import language_code
from typing import List
from google.cloud import dialogflow
from bot.scripts.message.finalize_response import finalize_response
from rich import print

from bot.setup.services.google_services import init_dialogflow

from google.cloud.dialogflow_v2beta1 import QueryInput, TextInput


"""
https://dialogflow.cloud.google.com/#/agent/{GOOGLE_CLOUD_PROJECT}/intents

select discordBot from the dropdown, top left

see also post_google_knowledge_response
"""


async def post_google_response(message):
    """ the dialog flow with the intents I set. """
    print("post_google_response")

    # t = random.randint(1, 100)

    author = message.author  # User
    # author_name = author.name  # Str
    channel = message.channel.name

    # attempt to get a response
    query = message.content
    query = (
        query.lower()  # .replace("rivers", "").replace("weezer", "").replace("bot", "")
    )
    replacers = ["rivers", "river", ","]
    for x in replacers:
        if query.startswith(x):
            query = query.replace(x, "", 1)
    response = detect_intent_texts([query], channel)
    # print(response)

    # # If conditions not met, return 'no we didn't do a googlebot response
    # else:
    #     return False

    # Also if it's just a default don't understand response
    # you can return no googlebot repsonse made.
    if (
        # (
        #     # Actually allow fallback responses in the q and a channel
        #     channel != "questions-and-help"
        #     and response.query_result.intent.display_name == "Default Fallback Intent"
        # )
        # or to block defaults even here:
        response.query_result.intent.display_name == "Default Fallback Intent"
        or response.query_result.intent is None
        or response is None
        or response.query_result.fulfillment_text == ""
    ):
        return False

    # Otherwise let's post this baby
    reply = response.query_result.fulfillment_text

    response = finalize_response(reply,  message.nick)

    await message.channel.send(response)

    # reply = author_name + ", " + reply
    # # print("!!!!!!!!!google")
    # print(f"Intent response: {reply}")
    # await message.channel.send(reply)
    return True


def detect_intent_texts(texts: List[str], channel: str):
    """Returns the result of detect intent with texts as inputs.

    Using the same `session_id` between requests allows continuation
    of the conversation."""
    print('detect_intent_texts')
    print(f"querying in the {channel} session.")

    # Initialize Dialogflow when needed
    sessions, session_client_knowledge, session_path_knowledge = init_dialogflow()

    # print(sessions)

    session = next((x["session"]
                   for x in sessions if x["id"] == channel), None)

    print("session", session)

    for text in texts:

        text = text[:255] if len(text) > 255 else text

        text_input = TextInput(
            text=text, language_code=language_code)

        query_input = QueryInput(text=text_input)

        try:
            response = session_client_knowledge.detect_intent(
                request={"session": session, "query_input": query_input}
            )
        except Exception as e:
            print(f"Error in detect_intent_texts: {e}")
            return None
        return response


def main():

    texts = ["Hi"]
    detect_intent_texts(texts)


if __name__ == "__main__":
    main()
