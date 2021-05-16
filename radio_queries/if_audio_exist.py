from firebase_admin import firestore, storage
from firebase_admin import credentials
from radio_queries import app_init_radio


class is_exist_fileName:
    def __init__(self, fileName):
        self.fileName = fileName
        self.cred = credentials.Certificate(r"C:\Users\gwan1\PycharmProjects\News_Project\serviceAccountKey.json")

    def is_exist(self):

        try:
            app_init = app_init_radio.App_init_radio(self.cred)
            app_init.is_app_init_radio()
        except Exception as e:
            print(e)

        firestore.client()
        bucket = storage.bucket().list_blobs()

        for audio in bucket:
            audio = audio.name
            if self.fileName == audio:
                return True
            else:
                continue

    # try:
    #     is_exist()
    # except Exception as e:
    #     print(e)
