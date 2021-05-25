import unittest

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

from news_data_queries import news_gothering_data
from Altinget_Data_Extracting import altinget_getHeadline, altinget_getContent, altinget_getDate
from news_scraping import altinget


def test_getNews_altinget():
    global headline, content, date, data_list, category, provider
    try:
        altinget.scrape_altinget(2)
        headline = altinget.headline
        content = altinget.content
        date = altinget.dt
        # firebase_admin.initialize_app(
        #     credentials.Certificate(r"C:\Users\gwan1\PycharmProjects\News_Project\serviceAccountKey.json"))
    except Exception as e:
        print(e)
    db = firestore.client()
    news_list = str(headline)
    docs = db.collection('altinget').where('headline', '==', headline).stream()
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
        assert news_list, a.strip()


try:
    test_getNews_altinget()
except Exception as e:
    print(e)
