import os
import sys
from google.oauth2 import service_account
from googleapiclient.discovery import build
from dotenv import load_dotenv
from rich import print
from google.cloud import dialogflow_v2beta1 as dialogflow
from bot.setup.services.dialogflow_sessions import init_dialogflow_sessions

# Load environment variables
load_dotenv()

sys.path.append("...")  # Adds higher directory to python modules path.


# Initialize Dialogflow sessions and clients
def init_dialogflow():
    """Initialize dialogflow clients and sessions"""
    sessions = init_dialogflow_sessions()

    session_id = "123456789"
    session_client_knowledge = dialogflow.SessionsClient()
    session_path_knowledge = session_client_knowledge.session_path(
        os.getenv("GOOGLE_CLOUD_PROJECT"), session_id
    )

    return sessions, session_client_knowledge, session_path_knowledge


def get_service(api_name, api_version, scopes, key_file_location):
    """Get a service that communicates to a Google API."""
    try:
        print("Trying to get credentials from env var GOOGLE_CREDENTIALS json object")
        credentials = service_account.Credentials.from_service_account_file(
            key_file_location)
    except Exception as e:
        print(f"Error loading credentials: {e}")
        return None

    # Apply scopes to the credentials
    scoped_credentials = credentials.with_scopes(scopes)

    # Build the service object
    service = build(api_name, api_version, credentials=scoped_credentials)
    print("Service built successfully")
    return service


def get_google_drive_service():
    """Get Google Drive API service."""
    SCOPES = ['https://www.googleapis.com/auth/drive']
    api_name = "drive"
    api_version = "v3"
    key_file_location = os.getenv("GOOGLE_DRIVE_CREDFILE")

    if not key_file_location:
        print("Google Drive credentials file not found in environment.")
        return None

    print(
        f"Getting Google Drive service... Credentials file location: {key_file_location}")
    return get_service(api_name, api_version, SCOPES, key_file_location)


def list_drive_files(service, page_size=10):
    """List files from Google Drive."""
    try:
        results = service.files().list(
            pageSize=page_size, fields="nextPageToken, files(id, name)"
        ).execute()
        items = results.get('files', [])

        if not items:
            print("No files found.")
        else:
            print("Files found:")
            for item in items:
                print(f"{item['name']} ({item['id']})")
    except Exception as e:
        print(f"Error listing files: {e}")


def list_permissions(service, file_id):
    """List permissions for a specific file in Google Drive."""
    try:
        response = service.permissions().list(
            supportsAllDrives=True,
            fileId=file_id,
            fields="permissions/id, permissions/emailAddress"
        ).execute()
        print(response)
    except Exception as e:
        print(f"Error listing permissions: {e}")


if __name__ == "__main__":
    # Example usage
    drive_service = get_google_drive_service()

    if drive_service:
        # List files
        list_drive_files(drive_service)

        # Example: List permissions for a specific folder
        green_nft_folder_id = "1hrNAl3tDX3Ui5BldZDrgCWxiRBL6NxtY"
        list_permissions(drive_service, green_nft_folder_id)


# # from oauth2client.service_account import ServiceAccountCredentials

# # from json.decoder import JSONDecodeError
# # import oauth2client
# # from oauth2client.service_account import ServiceAccountCredentials
# # from google.oauth2 import service_account
# # from google.auth import jwt

# load_dotenv()

# sys.path.append("...")  # Adds higher directory to python modules path.


# def get_service(api_name, api_version, scopes, key_file_location):
#     """Get a service that communicates to a Google API.

#     Args:
#         api_name: The name of the api to connect to.
#         api_version: The api version to connect to.
#         scopes: A list auth scopes to authorize for the application.
#         key_file_location: The path to a valid service account JSON key file.

#     Returns:
#         A service that is connected to the specified API.
#     """

#     try:
#         print("trying to get credentials from env var GOOGLE_CREDENTIALS json object")
#         # get the path to the json file
#         path = "C:\RC Dropbox\Rivers Cuomo\Apps\cuomputer\riverscuomo-8cc6d-1e794dddab08.json"

#         credentials = service_account.Credentials.from_service_account_info(
#             path)
#     except Exception as e:
#         print(e)
#         try:
#             print(
#                 f"failed...trying to get credentials from env var GOOGLE_CREDENTIALS json file at {key_file_location}")
#             credentials = service_account.Credentials.from_service_account_file(
#                 key_file_location)
#         except Exception as e:
#             print(e)

#             return None
#     print("credentials obtained")
#     scoped_credentials = credentials.with_scopes(scopes)

#     # Build the service object.
#     service = build(api_name, api_version, credentials=scoped_credentials)
#     print("service built")

#     return service


# def get_google_drive_service():
#     SCOPES = [
#         # 'https://www.googleapis.com/auth/spreadsheets',
#         'https://www.googleapis.com/auth/drive'
#     ]
#     api_name = "drive"
#     api_version = "v3"
#     key_file_location = os.environ.get("GOOGLE_DRIVE_CREDFILE")
#     print(f"get_google_drive_service...{key_file_location}")
#     return get_service(api_name, api_version, SCOPES, key_file_location)


# def main():

#     drive_service = get_google_drive_service()
#     print(drive_service)

#     # Call the Drive v3 API
#     results = drive_service.files().list(
#         pageSize=10, fields="nextPageToken, files(id, name)").execute()
#     items = results.get('files', [])

#     if not items:
#         print("No files found.")
#     else:
#         print("Files:")
#         for item in items:
#             print("{0} ({1})".format(item["name"], item["id"]))

#     exit()

#     green_nft_folder_id = "1hrNAl3tDX3Ui5BldZDrgCWxiRBL6NxtY"

#     # response = (
#     #     drive_service.permissions()
#     #     .create(
#     #         body={
#     #             "role": "writer",
#     #             "type": "user",
#     #             "emailAddress": "kyokoandrivers@gmail.com",
#     #             "useDomainAdminAccess": True,
#     #         },
#     #         fileId="1hrNAl3tDX3Ui5BldZDrgCWxiRBL6NxtY",
#     #         supportsAllDrives=True,
#     #     )
#     #     .execute()
#     # )

#     response = (
#         drive_service.permissions()
#         .list(
#             supportsAllDrives=True,
#             fileId=green_nft_folder_id,
#             fields="permissions/id, permissions/emailAddress",
#         )
#         .execute()
#     )

#     print(response)


# if __name__ == "__main__":
#     main()
