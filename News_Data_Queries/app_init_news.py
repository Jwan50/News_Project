import firebase_admin

from firebase_admin import credentials


def is_app_init_news():
    try:
        if not len(firebase_admin._apps):
            cred = credentials.Certificate(r"C:\Users\gwan1\PycharmProjects\News_Project Functional\serviceAccountKey.json")    # File containg connection parameters
            firebase_admin.initialize_app(cred)     # To initiate the Firebase app                                              # is separated for security

    except Exception as e:
        print(e)
