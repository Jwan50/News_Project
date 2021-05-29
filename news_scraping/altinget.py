import bs4 as bs
import datetime
import requests
from Altinget_Data_Extracting.altinget_getContent import altinget_getContent
from Altinget_Data_Extracting.altinget_getHeadline import altinget_getHeadline
from Altinget_Data_Extracting.altinget_getDate import altinget_getDate
from news_data_queries.news_gathering_data import gather_data

provider = 'altinget'
categories = {'kommunal'}
data_name = 'altinget'


def scrape_altinget(runType):
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
                dt = altinget_getDate(header, scrap_date)
                gather_data(headline, content, dt, provider, category, runType, data_name)
                print('Provider; ', provider, 'Headline: ', headline, ' Content: ', content, ' Date: ', dt)

        except Exception as e:
            print(e)
