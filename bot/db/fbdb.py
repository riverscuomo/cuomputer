import firebase_admin
from firebase_admin import credentials, firestore
import os
from dotenv import load_dotenv

load_dotenv()


class FirestoreDB:
    def __init__(self):
        self.project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
        self.cred_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
        self.cred = credentials.ApplicationDefault()

        if not firebase_admin._apps:  # Initialize Firebase app only if not already initialized
            firebase_admin.initialize_app(self.cred, {
                "projectId": self.project_id,
            })

        self.db = firestore.client()

    def get_db(self):
        return self.db


# Singleton instance of FirestoreDB class
_firestore_db_instance = None


def get_firestore_db():
    global _firestore_db_instance
    if _firestore_db_instance is None:
        _firestore_db_instance = FirestoreDB()
    return _firestore_db_instance.get_db()

# Example test function


def test():
    db = get_firestore_db()
    print(db)


# If you want to run a quick test
if __name__ == "__main__":
    test()


# import firebase_admin
# from firebase_admin import credentials
# from firebase_admin import firestore
# import os
# from dotenv import load_dotenv
# load_dotenv()

# print("fbdb.py init firestore")
# project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
# print(os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"))
# # If you have a cred dict set in the env
# # cred = credentials.Certificate(GOOGLE_APPLICATION_CREDENTIALS) # UNFORTUNATLEY CAN'T USE THIS BECUASE GOOGLE_APPLICATION_CREDENTIALS HAS TO BE SET IN ENV FOR DIALOGFLOW
# # Use the application default credentials
# cred = credentials.ApplicationDefault() # If you have a credfile set in the env

# firebase_admin.initialize_app(
#     cred,
#     {
#         "projectId": project_id,
#     },
# )

# db = firestore.client()

# def test():

#     cred = cred

#     firebase_admin.initialize_app(
#     cred,
#     {
#         "projectId": project_id,
#     },
# )

# if __name__ == "__main__":
#     test()
