
from bot.setup.services.google_services import init_dialogflow
from dotenv import load_dotenv
from bot.scripts.message.finalize_response import finalize_response
from google.cloud import dialogflow_v2beta1 as dialogflow_v2beta1
from config import *
from typing import List
import sys

sys.path.append("...")  # Adds higher directory to python modules path.
load_dotenv()


@DeprecationWarning
async def post_google_knowledge_response(message):
    """ 
    Appears to be dead?

    From interviews?    

    """
    print("post_knowledge_response")

    response = detect_intent_knowledge(message)
    # print(response)

    if response is None:
        return False

    # print(response.match_confidence_level)

    if (
        # response.match_confidence_level
        # == dialogflow_v2beta1.KnowledgeAnswers.Answer.MatchConfidenceLevel.HIGH
        # or response.match_confidence_level
        # == dialogflow_v2beta1.KnowledgeAnswers.Answer.MatchConfidenceLevel.MEDIUM
        response.match_confidence
        # > 8.9
        > .87
    ):

        # print(response)

        # Otherwise let's post this baby
        reply = response.answer
        reply = reply.split("\n")[0]
        reply = clean_message(reply)

        response = finalize_response(
            reply, message.nick)
        await message.channel.send(response)

        return True
        # reply = author_name + ", " + reply
        # # print("!!!!!!!!!google")
        # print(f"Knowledge response: {reply}")
        # await message.channel.send(reply)
        # return True
    # If conditions not met, return 'no we didn't do a googlebot response
    else:
        return False


def clean_message(reply):
    reply = reply.replace("!", ".")
    reply = reply.replace("(laughs)", "haha")
    reply = reply.replace("drugs", "ayurveda")
    reply = reply.replace("tits", "chest")
    return reply


def detect_intent_knowledge(message):
    """
    Returns the result of detect intent with querying Knowledge Connector.

    Args:
    project_id: The GCP project linked with the agent you are going to query.
    session_id: Id of the session, using the same `session_id` between requests
              allows continuation of the conversation.
    knowledge_base_id: The Knowledge base's id to query against.
    texts: A list of text queries to send.
    """

    text = message.content
    print("detect_intent_knowledge")
    sessions, openai_sessions, session_client_knowledge, session_path_knowledge = init_dialogflow()
    print(session_client_knowledge)
    # print(text)

    if len(text) > 255:
        text = text[:255]
    text_input = dialogflow_v2beta1.TextInput(
        text=text)
    query_input = dialogflow_v2beta1.QueryInput(text=text_input)
    knowledge_base_path = dialogflow_v2beta1.KnowledgeBasesClient.knowledge_base_path(
        os.environ.get("GOOGLE_CLOUD_PROJECT"), os.environ.get(
            "KNOWLEDGE_BASE_ID"),
    )
    query_params = dialogflow_v2beta1.QueryParameters(
        knowledge_base_names=[knowledge_base_path]
    )
    print(query_params)

    request = dialogflow_v2beta1.DetectIntentRequest(
        session=session_path_knowledge,
        query_input=query_input,
        query_params=query_params,
    )
    print(request)
    response = session_client_knowledge.detect_intent(request=request)
    print(response)

    # print("=" * 20)
    print(f"Query text: {response.query_result.query_text}")
    # print(
    #     "Detected intent: {} (confidence: {})\n".format(
    #         response.query_result.intent.display_name,
    #         response.query_result.intent_detection_confidence,
    #     )
    # )
    print(f"Fulfillment text: {response.query_result.fulfillment_text}\n")
    # print("Knowledge results:")
    knowledge_answers = response.query_result.knowledge_answers
    for answer in knowledge_answers.answers:
        print(f" - Answer: {answer.answer}")
        print(f" - Confidence: {answer.match_confidence}")
        break
    # print(knowledge_answers.answers)
    # print(knowledge_answers.answers[0])
    # print(knowledge_answers.answers[0].answer)
    try:
        return knowledge_answers.answers[0]
    except Exception as e:
        # print(e)
        return None


def main():

    texts = [
        "connie chung?",
        "who are you?",
        "do you sleep with groupies?",
        "What’s the video for “Hashpipe” like?",
    ]

    for text in texts:
        answer = detect_intent_knowledge(text)
        print(answer)


if __name__ == "__main__":
    main()
