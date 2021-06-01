import bs4 as bs
import datetime
import requests
from Berlingske_Data_Extracting.berlingske_getContent import berlingske_getContent
from Berlingske_Data_Extracting.berlingske_getHeadline import berlingske_getHeadline
from Berlingske_Data_Extracting.berlingske_getDate import berlingske_getDate
from news_data_queries.news_gathering_data import gather_data
from tests.test_headline import test_headline

provider = 'Berlingske'
categories = {'politik', 'sport', 'internationalt', 'samfund'}  # List of category to be scraped, excluding the rest of categories
data_name = 'berlingske'


def scrape_berlingske(runType):
    urlbase = "https://www.berlingske.dk/nyheder/"                          # The basic URL link
    scrap_date = datetime.datetime.now()
    for category in categories:
        urlbase_category = urlbase + category                               # Passing category to the URL
        try:
            urltxt = requests.get(urlbase_category)
            urltxt = urltxt.content
            soup = bs.BeautifulSoup(urltxt, 'html.parser')
            headers = soup.findAll('div', {'class': 'teaser-container'})   # 'div' tag with that class namecontains all headers
            for header in reversed(headers):                               # Reversed loop is to start the ealiest first

                headline = berlingske_getHeadline(header)                  # Passing header as parameter to getHeadline function in other file
                content = berlingske_getContent(header)                    # Passing header as parameter to getContent function in other file
                if content is None:
                    continue
                dt = berlingske_getDate(header, scrap_date)                # Passing header and scrap_date as dt parameter to getDate function in other file
                if not dt:
                    continue
                gather_data(headline, content, dt, provider, category, runType, data_name)  # Putting all together and passing all parameters to gather_data file
                print('Provider; ', provider, ' -Headline: ', headline, ' -Content: ', content, ' -Date: ', dt)
                test_headline(headline, data_name)                          # To do test for the headline
                if test_headline:
                    print('Tesing Equal Headline: succeeded')
                else:
                    print('Tesing Equal Headline: failed')
        except Exception as e:
            print(e)
