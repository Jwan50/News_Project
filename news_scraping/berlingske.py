import bs4 as bs
import datetime
import requests
from Berlingske_Data_Extracting.berlingske_getContent import berlingske_getContent
from Berlingske_Data_Extracting.berlingske_getHeadline import berlingske_getHeadline
from Berlingske_Data_Extracting.berlingske_getDate import berlingske_getDate
from news_data_queries.news_gathering_data import gather_data
from tests.test_headline import test_headline

provider = 'Berlingske'
categories = {'politik', 'sport', 'internationalt', 'samfund'}
data_name = 'berlingske'


def scrape_berlingske(runType):
    urlbase = 'https://www.berlingske.dk/nyheder/'
    scrap_date = datetime.datetime.now()
    for category in categories:
        urlbase_category = urlbase + category
        try:
            urltxt = requests.get(urlbase_category)
            urltxt = urltxt.content
            soup = bs.BeautifulSoup(urltxt, 'html.parser')
            headers = soup.findAll('div', {'class': 'teaser-container'})
            for header in reversed(headers):

                headline = berlingske_getHeadline(header)
                content = berlingske_getContent(header)
                dt = berlingske_getDate(header, scrap_date)
                if not dt:
                    continue
                gather_data(headline, content, dt, provider, category, runType, data_name)
                print('Provider; ', provider, ' -Headline: ', headline, ' -Content: ', content, ' -Date: ', dt)
                test_headline(headline, data_name)
                if test_headline:
                    print('Tesing Equal Headline: succeeded')
                else:
                    print('Tesing Equal Headline: failed')
        except Exception as e:
            print(e)
