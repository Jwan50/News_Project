import os
import bs4 as bs
import datetime
import requests
import shutil
from selenium import webdriver
from youtube_dl import YoutubeDL
from radio_queries import if_audio_exist
from radio_queries import playlist_saving
from radio_queries import if_playlist_exist
from radio_queries import save_audio_to_storage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By


class p4_bornholm_scraper:
    def __init__(self, scrape_back_days, runType):
        self.scrape_back_days = scrape_back_days
        self.runType = runType
        self.radioName = 'p4 bornholm'
        self.linkName = 'p4bornholm'
        self.songs_saved = 0
        self.songs_found = 0
        self.data_name = 'P4_playlist'
        self.removing_word = {'(Radio Edit)', '(Remix)', '(Edit)', '(Single Edit)',
                              '(Boogie Edit)', '(No Rap Edit)', '(Studio 2054 Remix)',
                              '(Radio Version)', '(Gettic Remix)', '(Metro Mix)', '?//'}

    def scrap_P4_bornholm(self):
        global dt, file_directory
        urlbase = 'https://www.dr.dk/playlister/'
        urlbase_name = urlbase + self.linkName + "/"
        today = datetime.datetime.now()
        run_end = today - datetime.timedelta(days=self.scrape_back_days)

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
                    for song in reversed(songs):
                        try:
                            if song.find('time') is None:
                                continue
                            if song.find('span', itemprop="byArtist").text:  # to insure that artist exists
                                artist = song.find('span', itemprop="byArtist").text.strip()
                            else:
                                continue

                            if song.find('a').text.strip():  # to insure that title exists
                                title = song.find('a').text.strip()
                            else:
                                continue

                            if "'" in artist:  # to avoid conflict with sql quote
                                artist = artist.replace("'", '')
                            if "'" in title:
                                title = title.replace("'", ' ')

                            for word in self.removing_word:
                                title = title.replace(word, '')
                            hm = song.find('time').text
                            hm_nat = float(hm.replace(':', '.'))
                            played_h_m = hm.split(':')
                            played_h = played_h_m[0]
                            played_m = played_h_m[1]

                            if soup.find('div', {
                                'class': 'playlist-program-details'}):  # because of p3 2021/02/ 09 and 10 natradio issue fixed
                                nat = soup.find('div', {'class': 'playlist-program-details'}).text.strip()
                                nat = nat.lower()
                                if 'i dag' not in nat:
                                    day = nat[13:15]
                                    dt = today.replace(day=int(day), hour=int(played_h), minute=int(played_m), second=0,
                                                       microsecond=0)
                                if 00.00 < hm_nat < 05.00 and 'i dag' in nat:
                                    _day = str(link_url).split('playlister/' + self.linkName + '/')[1]
                                    _day = _day[8:10]
                                    dt = today.replace(day=int(_day), hour=int(played_h), minute=int(played_m),
                                                       second=0,
                                                       microsecond=0)
                                if 05.00 < hm_nat < 24.00 and 'i dag' in nat:
                                    _day = str(link_url).split('playlister/' + self.linkName + '/')[1]
                                    _day = _day[8:10]
                                    dt = today.replace(day=int(_day), hour=int(played_h), minute=int(played_m),
                                                       second=0,
                                                       microsecond=0)
                            else:
                                dt = today.replace(hour=int(played_h), minute=int(played_m), second=0, microsecond=0)
                            if self.runType > 1:
                                audioName = artist + ' - ' + title + '.mp3'
                                fileName = str(audioName.lower())
                                try:
                                    if_audio_ex = if_audio_exist.is_exist_fileName(fileName).is_exist()
                                    if_playlist_ex = if_playlist_exist.is_playlist_exist(title, artist, dt,
                                                                                         self.data_name).is_playlist()
                                    if if_audio_ex:
                                        if if_playlist_ex:
                                            break
                                        try:
                                            playlist_sav = playlist_saving.playlist_to_Fir_p3(title, artist, dt,
                                                                                              fileName, self.data_name)
                                            playlist_sav.playlist_to_Fir()
                                        except Exception as e:
                                            print('')
                                    if if_audio_ex and if_playlist_ex:
                                        break
                                    else:
                                        tube_artist = artist.split(' ')
                                        tube_title = title.split(' ')
                                        play_link = 'https://www.youtube.com/results?search_query='
                                        for title_word in tube_title:
                                            play_link = play_link + title_word + '+'
                                        for artist_word in tube_artist:
                                            play_link = play_link + artist_word + '+'

                                        play_link = play_link[:-1]
                                        options = webdriver.ChromeOptions()
                                        browser = webdriver.Chrome(executable_path="C:\chromedriver.exe",
                                                                   options=options)
                                        browser.get(play_link)
                                        WebDriverWait(browser, 10).until(
                                            expected_conditions.visibility_of_element_located((By.XPATH,
                                                                                               '//*[@id="yDmH0d"]/c-wiz/div/div/div/div[2]/div[1]/div[4]/form/div[1]/div/button/div[2]'))).click()
                                        urltxt = browser.page_source
                                        soupTube = bs.BeautifulSoup(urltxt, 'html.parser')
                                        hrefs = soupTube.find_all('a', {
                                            'class': 'yt-simple-endpoint style-scope ytd-video-renderer'})[0]['href']
                                        To_play_url = 'https://www.youtube.com' + hrefs
                                        os.chdir("D:/TempAudFiles")

                                        audio_downloder = YoutubeDL({'format': 'bestaudio/best'})
                                        audio_downloder.extract_info(To_play_url)
                                        downloaded_temp = os.listdir("D:\TempAudFiles")
                                        for file in downloaded_temp:
                                            if file.lower().startswith(artist[:6].lower()) or file.lower().startswith(
                                                    title.lower()):
                                                os.rename(file, fileName.lower())
                                                file_directory = "D:\AudFiles" + "\\" + fileName
                                                dowloaded = os.listdir("D:\AudFiles")
                                                if fileName not in dowloaded:
                                                    shutil.move(('D:/TempAudFiles/' + fileName.lower()), "D:\AudFiles")
                                                downloaded_temp = os.listdir("D:\TempAudFiles")
                                                for file in downloaded_temp:
                                                    os.remove(file)
                                        save_audio = save_audio_to_storage.save_audio_p3(fileName, file_directory)
                                        try:
                                            save_audio.save_audio()
                                        except Exception as e:
                                            print(e)
                                        playlist_sav = playlist_saving.playlist_to_Fir_p3(title, artist, dt,
                                                                                          fileName, self.data_name)
                                        try:
                                            playlist_sav.playlist_to_Fir()
                                        except Exception as e:
                                            print(e)

                                        print('played at: ', dt, 'artist: ' + artist + ' -- ',
                                              'title: ' + title + ' -- ',
                                              ' -- ', 'radio name: ' + self.radioName)
                                except Exception as e:
                                    print(e)

                                    print('played at: ', dt, 'artist: ' + artist + ' -- ', 'title: ' + title + ' -- ',
                                          ' -- ', 'radio name: ' + self.radioName)
                                else:
                                    print('song: ' + title + ' - ' + artist + ' is already exists')
                            else:
                                print('played at: ', dt, 'artist: ' + artist + ' -- ', 'title: ' + title + ' -- ',
                                      ' -- ', 'radio name: ' + self.radioName)
                        except Exception as e:
                            print(e)
            except Exception as e:
                print(e)
            today = today - datetime.timedelta(days=1)

