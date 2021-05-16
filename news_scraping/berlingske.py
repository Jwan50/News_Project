import bs4 as bs
import datetime
import requests
from news_queries import news_saving


class Berlingske:
    def __init__(self, runType):
        self.runType = runType
        self.news_saved = 0
        self.news_found = 0
        self.provider = 'berlingske'
        self.categories = {'politik', 'sport', 'internationalt', 'samfund'}
        self.data_name = 'berlingske'

    def scrape_berlingske(self):

        urlbase = 'https://www.berlingske.dk/nyheder/'
        scrap_date = datetime.datetime.now()
        for category in self.categories:
            urlbase_category = urlbase + category
            try:
                urltxt = requests.get(urlbase_category)
                urltxt = urltxt.content
                soup = bs.BeautifulSoup(urltxt, 'html.parser')
                headers = soup.findAll('div', {'class': 'teaser-container'})
                for header in reversed(headers):
                    header_date = header.find('span', {'class': 'text-uppercase font-s2'}).text.lower()
                    if 'i går' in header_date.lower() or '/' in header_date:
                        continue
                    hm = header_date.split(':')
                    h = int(hm[0])
                    m = int(hm[1])
                    dt = scrap_date.replace(hour=h, minute=m, second=0, microsecond=0)
                    dt = dt.strftime('%Y-%m-%d')
                    dt = datetime.datetime.strptime(dt, '%Y-%m-%d')
                    headline = header.find('h4', {'class': 'teaser__title d-inline-block font-s4'}).text.strip()
                    hrefs = header.find('h4', {'class': 'teaser__title d-inline-block font-s4'})('a')[0]['href']
                    link_to_more = 'https://www.berlingske.dk' + hrefs
                    link_urltxt = requests.get(link_to_more)
                    link_urltxt = link_urltxt.content
                    soup = bs.BeautifulSoup(link_urltxt, 'lxml')
                    unwanted = soup.find('aside', {'class': 'embedded-element embedded-factbox position-relative'})
                    if unwanted:
                        unwanted.extract()
                    if not (soup.find('div', {'class': 'article-body'})):
                        continue
                    contents = soup.findAll('div', {'class': 'article-body'})[0]('p')

                    content = ''
                    for text in contents:
                        text = text.text.strip()
                        if 'ritzau' in text:
                            break
                        content = content + ' ' + text
                        if 'Fold sammen' in content:
                            content = content.split('Fold sammen')
                            content = content[0]

                    if self.runType > 1:
                        try:
                            news_saving_ber = news_saving.news_saving(self.provider, headline, content, dt,
                                                                      category,
                                                                      self.data_name)
                            news_saving_ber.news_save()

                        except Exception as e:
                            print(e)
                    print(" --News source: {}, --Category: {}, -- Headline: {},  --Date: {}".format(self.provider,
                                                                                                    category,
                                                                                                    headline, dt))
            except Exception as e:
                print(e)
