import firebase
import firebase_admin
from firebase_admin import credentials, firestore, storage


def is_exist(fileName):
    if not len(firebase_admin._apps):
        cred = credentials.Certificate(r"C:\Users\gwan1\PycharmProjects\News_Project\serviceAccountKey.json")
        firebase_admin.initialize_app(cred, {'storageBucket': 'the-news-project.appspot.com'})
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
