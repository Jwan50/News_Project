import bs4 as bs
import datetime
import requests
import data_queries.news_saving

news_saved = 0
news_found = 0
provider = 'altinget'
months = {'januar': 1, 'februar': 2, 'marts': 3, 'april': 4, 'maj': 5, 'juni': 6, 'juli': 7, 'august': 8,
          'september': 9, 'oktober': 10, 'november': 11, 'december': 12}
categories = {'kommunal' 'boern', 'eu', 'kultur', 'arbejdsmarked', 'arktis', 'by', 'civilsamfund', 'digital'}
data_name = 'altinget'

def scrape_altinget(runType):
    global news_saved, news_found
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
                for month_danish in months:
                    if content_month_danish == month_danish:
                        month = str(months[content_month_danish])
                        dt = scrap_date.replace(day=int(day), month=int(month), year=int(year))
                        dt = dt.strftime('%Y-%m-%d')
                        dt = datetime.datetime.strptime(dt, '%Y-%m-%d')
                        break

                if runType > 1:
                    try:
                        data_queries.news_saving.news_save(provider, headline, content, dt, category, data_name)
                        if data_queries.news_saving.news_save:
                            news_saved += 1
                        else:
                            print("Altinget news for category: '{}', date: '{}' failed to save in data".format(category,
                                                                                                               dt))
                    except Exception as e:
                        print(e)
                    news_found += 1
                print(" --News source: {}, --Category: {}, -- Headline: {},  --Date: {}".format(provider, category,
                                                                                                headline, dt))
        except Exception as e:
            print(e)


try:
    scrape_altinget()
    print("news_found", news_found)
    print("news_saved", news_saved)
except Exception as e:
    print("news_found", news_found)
