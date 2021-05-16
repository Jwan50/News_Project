import bs4 as bs
import datetime
import requests
from news_queries import news_saving


class Altinget:
    def __init__(self, runType):
        self.runType = runType
        self.news_saved = 0
        self.news_found = 0
        self.provider = 'altinget'
        self.months = {'januar': 1, 'februar': 2, 'marts': 3, 'april': 4, 'maj': 5, 'juni': 6, 'juli': 7, 'august': 8,
                       'september': 9, 'oktober': 10, 'november': 11, 'december': 12}
        self.categories = {'kommunal', 'boern', 'eu', 'kultur', 'arbejdsmarked', 'arktis', 'by', 'civilsamfund',
                           'digital'}
        self.data_name = 'altinget'

    def scrape_altinget(self):
        global news_saved, news_found
        urlbase = "https://api.altinget.dk"
        scrap_date = datetime.datetime.now()
        for category in self.categories:
            urlbase_category = urlbase + '/' + category + '/artikel.aspx'
            try:
                urltxt = requests.get(urlbase_category)
                urltxt = urltxt.content
                soup = bs.BeautifulSoup(urltxt, 'html.parser')

                headers = soup.findAll('article', {'class': 'featured-article featured-article-minor'})
                for header in reversed(headers):
                    headline = header.find('h3', {'class': 'media-heading media-heading-article'}).text.strip()
                    content = header.find('p').text.strip()
                    if not content:
                        continue
                    content_date = header.find('time').text
                    content_date = content_date.split('.')
                    day = content_date[0]
                    year = content_date[1][-4:]
                    content_month_danish = content_date[1][:-4].strip().lower()
                    dt = ''
                    for month_danish in self.months:
                        if content_month_danish == month_danish:
                            month = str(self.months[content_month_danish])
                            dt = scrap_date.replace(day=int(day), month=int(month), year=int(year))
                            dt = dt.strftime('%Y-%m-%d')
                            dt = datetime.datetime.strptime(dt, '%Y-%m-%d')
                            break

                    if self.runType > 1:
                        news_saving_alt = news_saving.news_saving(self.provider, headline, content, dt,
                                                                  category,
                                                                  self.data_name)
                        try:
                            news_saving_alt.news_save()
                        except Exception as e:
                            print(e)
                    print(" --News source: {}, --Category: {}, -- Headline: {},  --Date: {}".format(self.provider,
                                                                                                    category,
                                                                                                    headline, dt))
            except Exception as e:
                print(e)

