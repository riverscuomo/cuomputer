# from oauth2client.service_account import ServiceAccountCredentials

# from json.decoder import JSONDecodeError
from oauth2client import file, client, tools
# import oauth2client
# from oauth2client.service_account import ServiceAccountCredentials
from httplib2 import Http
from googleapiclient.discovery import build
# from google.oauth2 import service_account
import os
from rich import print
# import json
# from google.auth import jwt
import sys

sys.path.append("...")  # Adds higher directory to python modules path.

def get_google_drive_service():
    print("get_google_drive_service...")
    print("if the file or folder isn't in MY DRIVE, you'll have to share it with knr?")
    # If modifying these scopes, delete the file token.json.
    SCOPES = "https://www.googleapis.com/auth/drive"

    store = file.Storage(os.environ.get("GOOGLE_DRIVE_CREDFILE"))

    

    # """ FIRST TIME YOU DEFINITELY STILL HAVE TO RUN THIS BLOCK INSTEAD"""
    # creds = None
    # if not creds or creds.invalid:
    #     print('creds not valid')
    #     # exit()
    #     flow = client.flow_from_clientsecrets(
    #         r'C:\RC Dropbox\Rivers Cuomo\Apps\credentials\client_secret_9xxx6-exxx5g.apps.googleusercontent.com.json', SCOPES)
    #     creds = tools.run_flow(flow, store)

    """ Thereafter: """
    creds = store.get()
    drive_service = build("drive", "v3", http=creds.authorize(Http()))
    # drive_service = build('drive', 'v3', credentials=creds)
    print(drive_service)

    return drive_service


def main():
    drive_service = get_google_drive_service()
    print(drive_service)

    # Call the Drive v3 API
    results = (
        drive_service.files()
        .list(pageSize=10, fields="nextPageToken, files(id, name)")
        .execute()
    )
    items = results.get("files", [])

    if not items:
        print("No files found.")
    else:
        print("Files:")
        for item in items:
            print("{0} ({1})".format(item["name"], item["id"]))

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
