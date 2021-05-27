from firebase_admin import firestore

from news_data_queries.news_saving import news_save


def is_news_exist(headline, content, dt, provider, category, data_name):
    db = firestore.client()
    result = db.collection(data_name).where('headline', '==', headline).where('category', '==', category).where(
            'date', '==', dt).get()
    if not result:
        news_save(provider, headline, content, dt, category, data_name)
    else:
        print('Exists: ', ' -Category: ', category, ' -Headline', headline, ' -Date', dt)
        return False
