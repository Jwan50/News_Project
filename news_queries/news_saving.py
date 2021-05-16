from firebase_admin import firestore

from firebase_admin import credentials
from news_queries import app_init_news


class news_saving:
    def __init__(self, provider, headline, content, dt, category, data_name):
        self.cred = credentials.Certificate(r"C:\Users\gwan1\PycharmProjects\News_Project\serviceAccountKey.json")
        self.provider = provider
        self.headline = headline
        self.content = content
        self.dt = dt
        self.category = category
        self.data_name = data_name

    def news_save(self):
        init_news = app_init_news.Init_news(self.cred)
        try:
            init_news.is_app_init_news()
            db = firestore.client()
            if db.collection(self.data_name).where('headline', '==', self.headline).where('category', '==',
                                                                                          self.category).where(
                    'date', '==', self.dt).get():
                return
            else:
                data = {'category': self.category,
                        'content': self.content,
                        'date': self.dt,
                        'headline': self.headline,
                        'provider': self.provider
                        }
                db.collection(self.data_name).add(data)
        except Exception as e:
            print('Problem sending data to: ' + self.data_name)
