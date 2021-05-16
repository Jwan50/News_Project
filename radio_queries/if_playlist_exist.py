import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


class is_playlist_exist:
    def __init__(self, title, artist, dt, data_name):
        self.title = title
        self.artist = artist
        self.dt = dt
        self.data_name = data_name

    def is_playlist(self):
        if not len(firebase_admin._apps):
            cred = credentials.Certificate(r"C:\Users\gwan1\PycharmProjects\News_Project\serviceAccountKey.json")
            firebase_admin.initialize_app(cred)
        db = firestore.client()

        if db.collection(self.data_name).where('date', '==', self.dt).where('title', '==', self.title).where('artist',
                                                                                                             '==',
                                                                                                             self.artist).get():
            return True
