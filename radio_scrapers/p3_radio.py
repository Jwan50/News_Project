import os
import bs4 as bs
import datetime
import requests
import shutil
from selenium import webdriver
from youtube_dl import YoutubeDL
from data_queries.if_audio_exist import is_exist
from data_queries.playlist_saving import playlist_to_Fir
from data_queries.save_audio_to_storage import save_audio
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from data_queries.if_playlist_exist import is_playlist

radioName = 'p3'
songs_saved = 0
songs_found = 0
data_name = 'P3_playlist'
removing_word = {'(Radio Edit)', '(Remix)', '(Edit)', '?//'}


def scrap_P3(scrape_back_days, runType):
    global songs_found, songs_saved, dt, file_directory

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

                        for word in removing_word:
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
                                day = nat[4:6]
                                dt = today.replace(day=int(day), hour=int(played_h), minute=int(played_m), second=0,
                                                   microsecond=0)
                            if 00.00 < hm_nat < 05.00 and 'i dag' in nat:
                                _day = str(link_url).split('playlister/' + radioName + '/')[1]
                                _day = _day[8:10]
                                dt = today.replace(day=int(_day), hour=int(played_h), minute=int(played_m), second=0,
                                                   microsecond=0)
                            if 05.00 < hm_nat < 24.00 and 'i dag' in nat:
                                _day = str(link_url).split('playlister/' + radioName + '/')[1]
                                _day = _day[8:10]
                                dt = today.replace(day=int(_day), hour=int(played_h), minute=int(played_m), second=0,
                                                   microsecond=0)
                        else:
                            dt = today.replace(hour=int(played_h), minute=int(played_m), second=0, microsecond=0)
                        if runType > 1:
                            audioName = artist + ' - ' + title + '.mp3'
                            fileName = str(audioName.lower())
                            try:
                                if is_exist(fileName):
                                    if is_playlist(title, artist, dt, data_name):
                                        break
                                    try:
                                        playlist_to_Fir(title, artist, dt, fileName, data_name)
                                    except Exception as e:
                                        print('')
                                if is_exist(fileName) and is_playlist(title, artist, dt, data_name):
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
                                    browser = webdriver.Chrome(executable_path="C:\chromedriver.exe", options=options)
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
                                        if file.lower().startswith(artist.lower()) or file.lower().startswith(
                                                title.lower()):
                                            os.rename(file, fileName.lower())
                                            file_directory = "D:\AudFiles" + "\\" + fileName
                                            dowloaded = os.listdir("D:\AudFiles")
                                            if fileName not in dowloaded:
                                                shutil.move(('D:/TempAudFiles/' + fileName.lower()), "D:\AudFiles")
                                            downloaded_temp = os.listdir("D:\TempAudFiles")
                                            for file in downloaded_temp:
                                                os.remove(file)
                                        if save_audio(fileName, file_directory):
                                            playlist_to_Fir(title, artist, dt, fileName, data_name)
                                        try:
                                            playlist_to_Fir(title, artist, dt, fileName, data_name)
                                        except Exception as e:
                                                print('')
                                        else:
                                            continue


                                    songs_saved += 1


                                    print('played at: ', dt, 'artist: ' + artist + ' -- ', 'title: ' + title + ' -- ',
                                          ' -- ', 'radio name: ' + radioName)
                            except Exception as e:
                                print(e)

                                print('played at: ', dt, 'artist: ' + artist + ' -- ', 'title: ' + title + ' -- ',
                                      ' -- ', 'radio name: ' + radioName)
                            else:
                                print('song: ' + title + ' - ' + artist + ' is already exists')
                        else:
                            songs_found += 1
                            print('played at: ', dt, 'artist: ' + artist + ' -- ', 'title: ' + title + ' -- ',
                                  ' -- ', 'radio name: ' + radioName)
                    except Exception as e:
                        print(e)
        except Exception as e:
            print(e)
        today = today - datetime.timedelta(days=1)


try:
    scrap_P3()
    print("songs_found", songs_found)
except Exception as e:
    print("songs_found", songs_found)
