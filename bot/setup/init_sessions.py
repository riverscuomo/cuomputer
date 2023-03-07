from google.cloud import dialogflow
import sys

sys.path.append("...")  # Adds higher directory to python modules path.
from config import all_response_channels
from rich import print
from dotenv import load_dotenv
import os
import json
load_dotenv()

# print("init_sessions.py")
# print(os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"))

# google_store = json.load(open(os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")))
# # session_client = dialogflow.SessionsClient().from_service_account_json(os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"))

# print(google_store)
# google_store["client_id"] = os.environ.get("GOOGLE_CLOUD_CLIENT_ID")
# google_store["private_key_id"] = os.environ.get("GOOGLE_CLOUD_PRIVATE_KEY_ID")
# google_store["private_key"] = os.environ.get("GOOGLE_CLOUD_PRIVATE_KEY")
# print(google_store)

# session_client = dialogflow.SessionsClient().from_service_account_info(google_store)


# credentials = dialogflow.from_service_account_file(os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"))

# OG
session_client = dialogflow.SessionsClient()

def init_sessions():
    """create a dialogflow conversation session for each channel
    the bot will be posting in"""

    sessions = []
    openai_sessions = {}
    for channel in all_response_channels:
        this_id = channel

        session = session_client.session_path(os.environ.get("GOOGLE_CLOUD_PROJECT"), this_id)

        session_data = {"id": this_id, "session": session}

        sessions.append(session_data)

        openai_sessions[channel]= ""

        # openai_sessions[channel]= {}



    print(f"openai_sessions={openai_sessions}")
    return sessions, openai_sessions


# Test function for module
def _test():
    init_sessions()


if __name__ == "__main__":
    _test()
