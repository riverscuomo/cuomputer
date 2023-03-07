import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import os
from dotenv import load_dotenv
load_dotenv()

print("fbdb.py init firestore")
project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
print(os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"))
# If you have a cred dict set in the env
# cred = credentials.Certificate(GOOGLE_APPLICATION_CREDENTIALS) # UNFORTUNATLEY CAN'T USE THIS BECUASE GOOGLE_APPLICATION_CREDENTIALS HAS TO BE SET IN ENV FOR DIALOGFLOW
# Use the application default credentials
cred = credentials.ApplicationDefault() # If you have a credfile set in the env

firebase_admin.initialize_app(
    cred,
    {
        "projectId": project_id,
    },
)

db = firestore.client()

def test():
    
    cred = cred

    firebase_admin.initialize_app(
    cred,
    {
        "projectId": project_id,
    },
)
    
if __name__ == "__main__":
    test()

