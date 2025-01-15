from google.cloud import dialogflow
import os
from config import all_response_channels
from dotenv import load_dotenv
load_dotenv()

session_client = dialogflow.SessionsClient()


def init_dialogflow_sessions():
    """Create a dialogflow conversation session for each channel."""
    sessions = []

    for channel in all_response_channels:
        this_id = channel
        session = session_client.session_path(
            os.environ.get("GOOGLE_CLOUD_PROJECT"), this_id)
        session_data = {"id": this_id, "session": session}
        sessions.append(session_data)

    return sessions

# Test function for module


def _test():
    from config import all_response_channels
    sessions = init_dialogflow_sessions(all_response_channels)
    print(sessions)


if __name__ == "__main__":
    _test()
