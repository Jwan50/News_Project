import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from radio_data_queries.playlist_saving import playlist_to_Fir


def is_playlist_exist(title, artist, dt, fileName, data_name):
    if not len(firebase_admin._apps):
        cred = credentials.Certificate(r"C:\Users\gwan1\PycharmProjects\News_Project Functional\serviceAccountKey.json")
        firebase_admin.initialize_app(cred)
    db = firestore.client()
    result = db.collection(data_name).where('date', '==', dt).where('title', '==', title).where('artist', '==',
                                                                                          artist).get()
    if not result:
        return True
    else:
        return False
