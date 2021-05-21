import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


class playlist_to_Fir:
    def __init__(self, title, artist, dt, fileName, data_name):
        self.title = title
        self.artist = artist
        self.dt = dt
        self.fileName = fileName
        self.data_name = data_name

    def playlist_to_Fir(self):
        if not len(firebase_admin._apps):
            cred = credentials.Certificate(r"C:\Users\gwan1\PycharmProjects\News_Project\serviceAccountKey.json")
            firebase_admin.initialize_app(cred)
        db = firestore.client()
        try:
            if not db.collection(self.data_name).where('date', '==', self.dt).where('title', '==', self.title).where(
                    'artist', '==',
                    self.artist).get():
                data = {'title': self.title,
                        'artist': self.artist,
                        'date': self.dt,
                        'fileName': self.fileName
                        }
                db.collection(self.data_name).add(data)
        except Exception as e:
            print('Problem sending data to: ' + self.data_name)
