import firebase_admin
from firebase_admin import credentials


def is_app_init_radio():
    try:
        if not len(firebase_admin._apps):
            cred = credentials.Certificate(r"C:\Users\gwan1\PycharmProjects\News_Project Functional\serviceAccountKey.json")
            firebase_admin.initialize_app(cred, {'storageBucket': 'the-news-project.appspot.com'})
            return True

    except Exception as e:
        print(e)
