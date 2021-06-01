import firebase_admin
from firebase_admin import credentials


def is_app_init_radio():
    try:
        if not len(firebase_admin._apps):
            cred = credentials.Certificate(r"C:\Users\gwan1\PycharmProjects\News_Project Functional\serviceAccountKey.json")                                # File containg connection parameters
            firebase_admin.initialize_app(cred, {'storageBucket': 'the-news-project.appspot.com'})    # To initiate the Firebase app                        # is separated for security
            return True

    except Exception as e:
        print(e)
