import firebase_admin
from firebase_admin import credentials, firestore, storage
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import bs4 as bs
from youtube_dl import YoutubeDL
import os
import shutil
from selenium.webdriver.common.by import By


def save_audio(artist, title, fileName, file_directory):
    if not len(firebase_admin._apps):
        cred = credentials.Certificate(r"C:\Users\gwan1\PycharmProjects\News_Project\serviceAccountKey.json")
        firebase_admin.initialize_app(cred)
    firestore.client()
    bucket = storage.bucket()
    blob = bucket.blob(fileName)
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
        expected_conditions.visibility_of_element_located(
            (By.XPATH, '//*[@id="yDmH0d"]/c-wiz/div/div/div/div[2]/div[1]/div[4]/form/div[1]/div/button/span'))).click()

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
    try:
        with open(file_directory, 'rb') as audioFiles:
            blob.upload_from_file(audioFiles, content_type='audio/mpeg')
    except Exception as e:
        print('Audio {} was not saved to storage: '.format(fileName) + ': ' + e)
