import firebase_admin


class App_init_radio:
    def __init__(self, cred):
        self.cred = cred

    def is_app_init_radio(self):
        try:
            if not len(firebase_admin._apps):
                firebase_admin.initialize_app(self.cred, {'storageBucket': 'the-news-project.appspot.com'})

        except Exception as e:
            print(e)
