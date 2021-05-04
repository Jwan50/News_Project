from firebase_admin import firestore

from news_queries.app_init_news import is_app_init_news


def news_save(provider, headline, content, dt, category, data_name):
    try:
        is_app_init_news()
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
