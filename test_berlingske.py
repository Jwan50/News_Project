import unittest

import firebase_admin
from firebase_admin import credentials
from news_builder import berlingske_building
from firebase_admin import firestore
from news_builder.berlingske_building import ber_news_building


class test_Altinget(unittest.TestCase):

    def test_getNews_belingske(self):
        global headline, content, date, data_list, category, provider
        try:
            ber_news_building(2).getNews_berlingske()
            category = berlingske_building.ber_news_building(2).news.category
            headline = berlingske_building.ber_news_building(2).news.headline
            content = berlingske_building.ber_news_building(2).news.content
            date = berlingske_building.ber_news_building(2).news.date
            provider = berlingske_building.ber_news_building(2).news.provider
            firebase_admin.initialize_app(credentials.Certificate(r"C:\Users\gwan1\PycharmProjects\News_Project\serviceAccountKey.json"))

        except Exception as e:
            print(e)
        db = firestore.client()

        news_list = str(headline)
        docs = db.collection('berlingske').where('headline', '==', headline).stream()
        for doc in docs:
            a = u'{} => {}'.format(doc.id, doc.to_dict())
            a = a.split("=>")
            a = a[1]
            a = a.split("headline': ")
            a = str(a[1])
            if "\xa0" in a:
                a = a.replace("\xa0", " ")
            a = a.replace(u"'", u"")

            if 'content' in a:
                a = a.split(", content:")
                a = a[0]
            if 'provider' in a:
                a = a.split(", provider:")
                a = a[0]
            if 'category' in a:
                a = a.split(", category:")
                a = a[0]

            if 'date' in a:
                a = a.split(", date:")
                a = a[0]
            if "}" in a:
                a = a.replace("}", " ")

            a = a.replace(u"'", u"")

            self.assertEqual(news_list, a.strip())
