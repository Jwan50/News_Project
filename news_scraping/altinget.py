import bs4 as bs
import datetime
import requests
from Altinget_Data_Extracting.altinget_getContent import altinget_getContent
from Altinget_Data_Extracting.altinget_getHeadline import altinget_getHeadline
from Altinget_Data_Extracting.altinget_getDate import altinget_getDate
from news_data_queries.news_gathering_data import gather_data
from tests.test_headline import test_headline

provider = 'altinget'
categories = {'kommunal', 'boern', 'eu', 'kultur', 'arbejdsmarked', 'arktis', 'by', 'civilsamfund', 'digital'}  # List of category to be scraped, excluding the rest of categories
data_name = 'altinget'


def scrape_altinget(runType):
    urlbase = "https://api.altinget.dk"                                                                 # The basic URL link
    scrap_date = datetime.datetime.now()                                                                 # Today's date now
    for category in categories:
        urlbase_category = urlbase + '/' + category + '/artikel.aspx'   # Passing category to the URL
        try:
            urltxt = requests.get(urlbase_category)
            urltxt = urltxt.content
            soup = bs.BeautifulSoup(urltxt, 'html.parser')
            headers = soup.findAll('article', {'class': 'featured-article featured-article-minor'})     # Targeting HTML tag called 'article' which contains all headers
            for header in reversed(headers):                                                            # Reversed loop is to start the ealiest first
                content = altinget_getContent(header)                                                   # Passing header as parameter to getContent function in other file
                if not content:                                                                         # To ignor news with no content
                    continue
                headline = altinget_getHeadline(header)                                                 # Passing header as parameter to getHeadline function in other file
                dt = altinget_getDate(header, scrap_date)                                               # Passing header and scrap_date as dt parameter to getDate function in other file
                if not dt:                                                                              # To ignor news with no date
                    continue
                gather_data(headline, content, dt, provider, category, runType, data_name)              # Putting all together and passing all parameters to gather_data file
                print('Provider; ', provider, 'Headline: ', headline, ' Content: ', content, ' Date: ', dt)
                test_headline(headline, provider)                                                       # To do test for the headline
                if test_headline:
                    print('Tesing Equal Headline: succeeded')
                else:
                    print('Tesing Equal Headline: failed')

        except Exception as e:
            print(e)
