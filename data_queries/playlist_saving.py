import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


def playlist_to_Fir(title, artist, dt, fileName, data_name):
    if not len(firebase_admin._apps):
        cred = credentials.Certificate(r"C:\Users\gwan1\PycharmProjects\News_Project\serviceAccountKey.json")
        firebase_admin.initialize_app(cred)
    db = firestore.client()
    try:
        if not db.collection(data_name).where('date', '==', dt).where('title', '==', title).where('artist', '==',
                                                                                                  artist).get():
            data = {'title': title,
                    'artist': artist,
                    'date': dt,
                    'fileName': fileName
                    }
            db.collection(data_name).add(data)
    except Exception as e:
        print('Problem sending data to: ' + data_name)
