import bs4 as bs
import datetime
import requests
from data_queries.news_saving import news_save

news_saved = 0
news_found = 0
provider = 'berlingske'
categories = {'politik', 'sport', 'internationalt', 'samfund'}
# runType = 2
data_name = 'berlingske'


def scrape_berlingske(runType):
    global news_saved
    global news_found
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

                if runType > 1:
                    try:
                        news_save(provider, headline, content, dt, category, data_name)
                        if news_save:
                            news_saved += 1
                        else:
                            print(
                                "Berlingski news for category: '{}', date: '{}' failed to save in data".format(category,
                                                                                                               dt))
                    except Exception as e:
                        print(e)
                    news_found += 1
                print(" --News source: {}, --Category: {}, -- Headline: {},  --Date: {}".format(provider, category,
                                                                                                headline, dt))
        except Exception as e:
            print(e)


try:
    scrape_berlingske()
    print("news_found", news_found)
    print("news_saved", news_saved)
except Exception as e:
    print("news_found", news_found)
