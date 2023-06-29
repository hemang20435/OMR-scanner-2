# firebase admin
import firebase_admin

# utils
import pathlib

# decouple
from decouple import config

# firebase modules
from firebase_admin import credentials, storage, firestore

ROOT_DIR: str = pathlib.Path(__file__).parent.parent.parent.resolve()
BUCKET_NAME: str = config("BUCKET_NAME", cast=str)

# Initialize firebase app and bucket
firebase_credentials = credentials.Certificate(f"{ROOT_DIR}/fb-credentials.json")
firebase_app = firebase_admin.initialize_app(
    firebase_credentials, {"storageBucket": BUCKET_NAME}
)
storageBucket = storage.bucket()
store_client = firestore.client(app=firebase_app)
