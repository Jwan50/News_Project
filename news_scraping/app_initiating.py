import firebase_admin
from firebase_admin import credentials


def is_app_initiated():
    try:
        if not len(firebase_admin._apps):
            cred = credentials.Certificate(r"C:\Users\gwan1\PycharmProjects\News_Project\serviceAccountKey.json")
            firebase_admin.initialize_app(cred)
        # db = firestore.client()
    except Exception as e:
        print(e)
