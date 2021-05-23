import firebase_admin
from firebase_admin import credentials


class Init_news:
    def __init__(self):
        self.cred = credentials.Certificate(r"C:\Users\gwan1\PycharmProjects\News_Project\serviceAccountKey.json")

    def is_app_init_news(self):
        try:
            if not len(firebase_admin._apps):
                firebase_admin.initialize_app(self.cred)

        except Exception as e:
            print(e)
