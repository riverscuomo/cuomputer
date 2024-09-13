# from google.cloud import dialogflow
# import sys

# sys.path.append("...")  # Adds higher directory to python modules path.
# from config import channels, all_response_channels
# from rich import print
# from dotenv import load_dotenv
# import os
# import json
# load_dotenv()


# session_client = dialogflow.SessionsClient()

# def init_sessions():
#     """create a dialogflow conversation session for each channel
#     the bot will be posting in"""

#     sessions = []

#     for channel in all_response_channels:

#         this_id = channel

#         # for dialogflow
#         session = session_client.session_path(os.environ.get("GOOGLE_CLOUD_PROJECT"), this_id)

#         session_data = {"id": this_id, "session": session}

#         sessions.append(session_data)

#     openai_sessions = {id: [] for channel_name, id in channels.items()}
#     print(f"openai_sessions={openai_sessions}")
#     return sessions, openai_sessions


# # Test function for module
# def _test():
#     init_sessions()


# if __name__ == "__main__":
#     _test()
