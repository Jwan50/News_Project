import bs4 as bs
import datetime
import requests
from P3_Data_Extracting.p3_getTitle import p3_getTitle
from P3_Data_Extracting.p3_getArtist import p3_getArtist
from P3_Data_Extracting.p3_getDate import p3_getDate
from radio_data_queries.radio_gothering_data import radio_gathering_data

radioName = 'p3'
linkName = 'p3'
data_name = 'P3_playlist'


def scrap_P3(scrape_back_days, runType):
    urlbase = 'https://www.dr.dk/playlister/'
    urlbase_name = urlbase + radioName + "/"
    today = datetime.datetime.now()
    run_end = today - datetime.timedelta(days=scrape_back_days)

    while run_end <= today:
        try:
            scrap_start = today.strftime("%Y,%m,%d")
            url = urlbase_name + scrap_start
            urltxt = requests.get(url)
            urltxt = urltxt.content
            soup = bs.BeautifulSoup(urltxt, 'lxml')
            ids_group = soup.findAll('div', {'class': 'span-3'})
            links = ids_group[0]('a')
            for link in reversed(links):
                link_url = link['href']
                url_new = 'https://www.dr.dk' + link_url
                urltxt_new = requests.get(url_new)
                urltxt_new = urltxt_new.content.decode("utf-8", "ignore")
                soup = bs.BeautifulSoup(urltxt_new, 'lxml')
                songs = soup.findAll('li', {'class': 'track'})
                if not songs:
                    continue
                else:
                    for song in reversed(songs):
                        try:
                            artist = p3_getArtist(song)
                            title = p3_getTitle(song)
                            dt = p3_getDate(song, soup, today, link_url, linkName)
                            radio_gathering_data(artist, title, dt, runType, data_name)
                        except Exception as e:
                            print(e)
        except Exception as e:
            print(e)
        today = today - datetime.timedelta(days=1)
