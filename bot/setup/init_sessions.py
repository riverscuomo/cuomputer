from google.cloud import dialogflow
import sys

sys.path.append("...")  # Adds higher directory to python modules path.
from config import all_response_channels
from rich import print
from dotenv import load_dotenv
import os
load_dotenv()


session_client = dialogflow.SessionsClient()
print(session_client)


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
