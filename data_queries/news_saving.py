import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


def news_save(provider, headline, content, dt, category, data_name):
    try:
        if not len(firebase_admin._apps):
            cred = credentials.Certificate(r"C:\Users\gwan1\PycharmProjects\News_Project\serviceAccountKey.json")
            firebase_admin.initialize_app(cred)
        db = firestore.client()
        try:
            if db.collection(data_name).where('headline', '==', headline).where('category', '==', category).where(
                    'date', '==', dt).get():
                return
            else:
                data = {'category': category,
                        'content': content,
                        'date': dt,
                        'headline': headline,
                        'provider': provider
                        }
                db.collection(data_name).add(data)
        except Exception as e:
            print('Problem sending data to: ' + data_name)


    except Exception as e:
        print(e)
