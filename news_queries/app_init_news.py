import firebase_admin


class Init_news:
    def __init__(self, cred):
        self.cred = cred

    def is_app_init_news(self):
        try:
            if not len(firebase_admin._apps):
                firebase_admin.initialize_app(self.cred)

        except Exception as e:
            print(e)
