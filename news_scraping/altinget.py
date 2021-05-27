import bs4 as bs
import datetime
import requests
from Altinget_Data_Extracting.altinget_getContent import altinget_getContent
from Altinget_Data_Extracting.altinget_getHeadline import altinget_getHeadline
from Altinget_Data_Extracting.altinget_getDate import altinget_getDate
from news_data_queries.news_gothering_data import news_gothering_data
from firebase_admin import firestore
import unittest

from tests.test_altinget import test_getNews_altinget

provider = 'altinget'
categories = {'kommunal'}
data_name = 'altinget'


def scrape_altinget(runType):
    global header
    urlbase = "https://api.altinget.dk"
    scrap_date = datetime.datetime.now()
    for category in categories:
        urlbase_category = urlbase + '/' + category + '/artikel.aspx'
        try:
            urltxt = requests.get(urlbase_category)
            urltxt = urltxt.content
            soup = bs.BeautifulSoup(urltxt, 'html.parser')
            headers = soup.findAll('article', {'class': 'featured-article featured-article-minor'})
            for header in reversed(headers):
                content = altinget_getContent(header)
                if not content:
                    continue
                headline = altinget_getHeadline(header)
                test_getNews_altinget(headline)
                dt = altinget_getDate(header, scrap_date)
                news_gothering_data(headline, content, dt, provider, category, runType, data_name)

        except Exception as e:
            print(e)