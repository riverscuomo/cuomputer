# from oauth2client.service_account import ServiceAccountCredentials

# from json.decoder import JSONDecodeError
import base64
from oauth2client import file, client, tools
# import oauth2client
# from oauth2client.service_account import ServiceAccountCredentials
from httplib2 import Http
from googleapiclient.discovery import build
# from google.oauth2 import service_account
import os
from rich import print
import json
# from google.auth import jwt
import sys

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2 import service_account
from dotenv import load_dotenv
load_dotenv()

sys.path.append("...")  # Adds higher directory to python modules path.

def get_service(api_name, api_version, scopes, key_file_location):
    """Get a service that communicates to a Google API.

    Args:
        api_name: The name of the api to connect to.
        api_version: The api version to connect to.
        scopes: A list auth scopes to authorize for the application.
        key_file_location: The path to a valid service account JSON key file.

    Returns:
        A service that is connected to the specified API.
    """

    try:  
        print("trying to get credentials from env var GOOGLE_CREDENTIALS json object")
        # get the path to the json file
        path = "C:\RC Dropbox\Rivers Cuomo\Apps\cuomputer\riverscuomo-8cc6d-1e794dddab08.json"

        credentials = service_account.Credentials.from_service_account_info(path)
    except Exception as e:
        print(e)
        try:
            print(f"failed...trying to get credentials from env var GOOGLE_CREDENTIALS json file at {key_file_location}")
            credentials = service_account.Credentials.from_service_account_file(
            key_file_location)
        except Exception as e:
            print(e)
            
            return None
    print("credentials obtained")
    scoped_credentials = credentials.with_scopes(scopes)

    # Build the service object.
    service = build(api_name, api_version, credentials=scoped_credentials)
    print("service built")

    return service

def get_google_drive_service():
    SCOPES = [
        # 'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
    ]
    api_name ="drive"
    api_version ="v3"
    key_file_location = os.environ.get("GOOGLE_DRIVE_CREDFILE")
    print(f"get_google_drive_service...{key_file_location}")
    return get_service(api_name, api_version, SCOPES, key_file_location)


# def get_google_drive_service():
#     print("get_google_drive_service...")
#     print("if the file or folder isn't in MY DRIVE, you'll have to share it with knr?")
#     # If modifying these scopes, delete the file token.json.
#     SCOPES = "https://www.googleapis.com/auth/drive"

#     store = file.Storage(os.environ.get("GOOGLE_DRIVE_CREDFILE"))
#     print(store)

    

#     # """ FIRST TIME YOU DEFINITELY STILL HAVE TO RUN THIS BLOCK INSTEAD"""
#     # creds = None
#     # if not creds or creds.invalid:
#     #     print('creds not valid')
#     #     # exit()
#     #     flow = client.flow_from_clientsecrets(
#     #         r'C:\RC Dropbox\Rivers Cuomo\Apps\credentials\client_secret_9xxx6-exxx5g.apps.googleusercontent.com.json', SCOPES)
#     #     creds = tools.run_flow(flow, store)

#     """ Thereafter: """
#     print("loading google drive creds from file...")
#     creds = store.get()
#     # print("os.environ.get('GOOGLE_DRIVE_CLIENT_ID')", os.environ.get("GOOGLE_DRIVE_CLIENT_ID"))
#     # creds.client_id = os.environ.get("GOOGLE_DRIVE_CLIENT_ID")
#     # print("os.environ.get('GOOGLE_DRIVE_CLIENT_SECRET')", os.environ.get("GOOGLE_DRIVE_CLIENT_SECRET"))
#     # creds.client_secret = os.environ.get("GOOGLE_DRIVE_CLIENT_SECRET")
#     # drive_service = build("drive", "v3", http=creds.authorize(Http()))
#     driver_service = build("drive", "v3", credentials=creds)
#     # drive_service = build('drive', 'v3', credentials=creds)
#     print(drive_service)

#     return drive_service


def main():

    drive_service = get_google_drive_service()
    print(drive_service)

    # Call the Drive v3 API
    results = drive_service.files().list(pageSize=10, fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])

    if not items:
        print("No files found.")
    else:
        print("Files:")
        for item in items:
            print("{0} ({1})".format(item["name"], item["id"]))

    exit()

    green_nft_folder_id = "1hrNAl3tDX3Ui5BldZDrgCWxiRBL6NxtY"

    # response = (
    #     drive_service.permissions()
    #     .create(
    #         body={
    #             "role": "writer",
    #             "type": "user",
    #             "emailAddress": "kyokoandrivers@gmail.com",
    #             "useDomainAdminAccess": True,
    #         },
    #         fileId="1hrNAl3tDX3Ui5BldZDrgCWxiRBL6NxtY",
    #         supportsAllDrives=True,
    #     )
    #     .execute()
    # )

    response = (
        drive_service.permissions()
        .list(
            supportsAllDrives=True,
            fileId=green_nft_folder_id,
            fields="permissions/id, permissions/emailAddress",
        )
        .execute()
    )

    print(response)


if __name__ == "__main__":
    main()
