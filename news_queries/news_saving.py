from firebase_admin import firestore


class news_saving:
    def __init__(self, provider, headline, content, date, category, data_name):

        self.provider = provider
        self.headline = headline
        self.content = content
        self.date = date
        self.category = category
        self.data_name = data_name

    def news_save(self):
        try:
            db = firestore.client()
            data_list = db.collection('altinget').where('headline', '==', self.headline).where('category', '==',
                                                                                               self.category).where(
                'date', '==', self.date).get()
            if data_list:
                return True
            else:
                data = {'category': self.category,
                        'content': self.content,
                        'date': self.date,
                        'headline': self.headline,
                        'provider': self.provider
                        }
                db.collection(self.data_name).add(data)
        except Exception as e:
            print('Problem sending data to: ' + self.data_name)
