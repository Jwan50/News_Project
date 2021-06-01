import bs4 as bs
import datetime
import requests
from P3_Data_Extracting.p3_getTitle import p3_getTitle
from P3_Data_Extracting.p3_getArtist import p3_getArtist
from P3_Data_Extracting.p3_getDate import p3_getDate
from Radio_Data_Queries.radio_gathering_data import radio_gathering_data

radioName = 'p3'
linkName = 'p3'
data_name = 'P3_playlist'


def scrap_P3(scrape_back_days, runType):
    urlbase = 'https://www.dr.dk/playlister/'                           # Common link between P3 and P4
    urlbase_name = urlbase + radioName + "/"                            # Adding the radio name to the common link
    today = datetime.datetime.now()                                     # The time now
    run_end = today - datetime.timedelta(days=scrape_back_days)         # Go to where we need to scape

    while run_end <= today:
        try:
            scrap_start = today.strftime("%Y,%m,%d")                    # Converting to string format with only Y - m - d
            url = urlbase_name + scrap_start                            # Adding the date of scraping to the url to target the right webpage of that date
            urltxt = requests.get(url)                                  # Reuests to get Json file
            urltxt = urltxt.content                                     # Target the content property of the comming Json
            soup = bs.BeautifulSoup(urltxt, 'lxml')                     # To reconstruct the Json file to be as html tree for easier browsing
            ids_group = soup.findAll('div', {'class': 'span-3'})
            links = ids_group[0]('a')                                   # Here we found all the list of links based on each program of the day
            for link in reversed(links):
                link_url = link['href']                                 # Get the link of each program
                url_new = 'https://www.dr.dk' + link_url                # Building a new url to go to each link seperately
                urltxt_new = requests.get(url_new)
                urltxt_new = urltxt_new.content.decode("utf-8", "ignore")
                soup = bs.BeautifulSoup(urltxt_new, 'lxml')
                songs = soup.findAll('li', {'class': 'track'})          # Playlists are here
                if not songs:
                    continue
                else:
                    for song in reversed(songs):
                        try:
                            artist = p3_getArtist(song)                                         # Call p3_getArtist function
                            title = p3_getTitle(song)                                           # Call p3_getTitle function
                            dt = p3_getDate(song, soup, today, link_url, linkName)              # Call p3_getDate function
                            radio_gathering_data(artist, title, dt, runType, data_name)         # Gathering all together
                        except Exception as e:
                            print(e)
        except Exception as e:
            print(e)
        today = today - datetime.timedelta(days=1)                                              # Go backward one day
