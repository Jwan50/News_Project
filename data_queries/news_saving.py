import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

from news_scraping.app_initiating import is_app_initiated


def news_save(provider, headline, content, dt, category, data_name):
    try:
        is_app_initiated()
        db = firestore.client()
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
