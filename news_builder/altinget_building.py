from news.concrete_news_builder import Concrete_news_builder
from news_queries import news_saving, app_init_news
import bs4 as bs
import datetime
import requests


class alt_concretenews_building(Concrete_news_builder):
    provider = 'altinget'
    months = {'januar': 1, 'februar': 2, 'marts': 3, 'april': 4, 'maj': 5, 'juni': 6, 'juli': 7, 'august': 8,
              'september': 9, 'oktober': 10, 'november': 11, 'december': 12}
    categories = {'kommunal', 'boern', 'eu', 'kultur', 'arbejdsmarked', 'arktis', 'by', 'civilsamfund', 'digital'}
    data_name = 'altinget'

    def __init__(self, runType):
        super().__init__()
        self.runType = runType

    def getNews_altinget(self):
        global headline, category, content, date, news
        urlbase = "https://api.altinget.dk"
        scrap_date = datetime.datetime.now()
        for category in self.categories:
            super().setCategory(category).build()
            urlbase_category = urlbase + '/' + 'kommunal' + '/artikel.aspx'
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
                    date = ''
                    for month_danish in self.months:
                        if content_month_danish == month_danish:
                            month = str(self.months[content_month_danish])
                            date = scrap_date.replace(day=int(day), month=int(month), year=int(year))
                            date = date.strftime('%Y-%m-%d')
                            date = datetime.datetime.strptime(date, '%Y-%m-%d')
                            break

                    if self.runType > 1:
                        init_app = app_init_news.Init_news()
                        news = super().setCategory(category).setHeadline(headline).setContent(content).setDate(
                            date).setProvider(provider=self.provider).build()

                        news_saving_alt = news_saving.news_saving(news.provider, news.headline, news.content, news.date,
                                                                  news.category, self.data_name)
                        try:
                            init_app.is_app_init_news()
                            news_saving_alt.news_save()
                        except Exception as e:
                            print(e)
                    print(" --News source: {}, --Category: {}, -- Headline: {},  --Date: {}".format(news.provider,
                                                                                                    news.category,
                                                                                                    news.headline,
                                                                                                    news.date))
            except Exception as e:
                print(e)
