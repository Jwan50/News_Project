
from firebase_admin import firestore, storage

from radio_queries.app_init_radio import is_app_init_radio


def is_exist(fileName):

    try:
        is_app_init_radio()
    except Exception as e:
        print(e)

    firestore.client()
    bucket = storage.bucket().list_blobs()

    for audio in bucket:
        audio = audio.name
        if fileName == audio:
            return True
        else:
            continue


try:
    is_exist()
except Exception as e:
    print(e)
