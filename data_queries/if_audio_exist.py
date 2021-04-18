import firebase
import firebase_admin
from firebase_admin import credentials, firestore, storage

from data_queries.app_init_radio import is_app_init_radio


def is_exist(fileName):
    try:
        is_app_init_radio()
    except Exception as e:
        print(e)

    db = firestore.client()
    bucket = storage.bucket().list_blobs()
    for audio in bucket:
        audio = str(audio)
        if fileName == audio:
            return
        else:
            continue


try:
    is_exist()
except Exception as e:
    print(e)
