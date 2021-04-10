import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


def playlist_to_Fir(title, artist, dt, fileName, data_name):
    try:
        if not len(firebase_admin._apps):
            cred = credentials.Certificate(
                "C:/Users\gwan1\Desktop\Pycharm workspace\\NewsProject-Scraper\serviceAccountKey.json")
            firebase_admin.initialize_app(cred)
        db = firestore.client()
        try:
            if db.collection(data_name).where('date', '==', dt).where('title', '==', title).where('artist', '==',
                                                                                                  artist).get():
                return
            else:
                data = {'title': title,
                        'artist': artist,
                        'date': dt,
                        'fileName': fileName
                        }
                db.collection(data_name).add(data)
        except Exception as e:
            print('Problem sending data to: ' + data_name)


    except Exception as e:
        print(e)
