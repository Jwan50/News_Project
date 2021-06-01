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
    if not len(firebase_admin._apps):                   # If app not initiated, so initiate it
        cred = credentials.Certificate(r"C:\Users\gwan1\PycharmProjects\News_Project Functional\serviceAccountKey.json")    # Directory to file containg connection parameter
        firebase_admin.initialize_app(cred)             # Initiate the app
    firestore.client()
    bucket = storage.bucket()                           # Local veriable for storage buckets
    blob = bucket.blob(fileName)                        # Get the audio file
    tube_artist = artist.split(' ')                     # When spliting the Artist name, we get a list.
    tube_title = title.split(' ')                       # Do same as above
    play_link = 'https://www.youtube.com/results?search_query= '    # The URL of YouTube when entending to search for any element
    for title_word in tube_title:
        play_link = play_link + title_word + '+'                    # Adding the list of element of artist name to pass it after to YouTube search bar
    for artist_word in tube_artist:
        play_link = play_link + artist_word + '+'                   # Adding the list of element of title name to pass it after to YouTube search bar

    play_link = play_link[:-1]                                      # To remove the last +
    options = webdriver.ChromeOptions()                             # WebDrive used to handle new page opening
    browser = webdriver.Chrome(executable_path="C:\chromedriver.exe", options=options)  # Call WebDrive to run
    browser.get(play_link)
    WebDriverWait(browser, 10).until(                               # Here, a click() function is passed to click the cookies consent
        expected_conditions.visibility_of_element_located(
            (By.XPATH, '//*[@id="yDmH0d"]/c-wiz/div/div/div/div[2]/div[1]/div[4]/form/div[1]/div/button/span'))).click()

    urltxt = browser.page_source
    soupTube = bs.BeautifulSoup(urltxt, 'html.parser')
    hrefs = soupTube.find_all('a', {                                # Getting the list of all maching elements found after searching in YouTube
        'class': 'yt-simple-endpoint style-scope ytd-video-renderer'})[0]['href']       # 0 index to choose the first index
    To_play_url = 'https://www.youtube.com' + hrefs                 # Creating the link of the song found after the above search
    os.chdir("D:/TempAudFiles")                                     # Change the default saving location to D:/TempAudFiles as temporary location

    audio_downloder = YoutubeDL({'format': 'bestaudio/best'})       # Parameter to be best audio
    audio_downloder.extract_info(To_play_url)                       # Start to download the audio
    downloaded_temp = os.listdir("D:\TempAudFiles")                 # List all the audios in the temporary location
    for file in downloaded_temp:
        if file.lower().startswith(artist[:6].lower()) or file.lower().startswith(      # Matching the audio file
                title.lower()):
            os.rename(file, fileName.lower())                       # If found, rename it so to remove the name of file which was give by youtube downloader
            file_directory = "D:\AudFiles" + "\\" + fileName        # Lis of audio which were downloaded ealier
            dowloaded = os.listdir("D:\AudFiles")
            if fileName not in dowloaded:                           # If not downloaded earlier. so move the newly downloaded to the downloaded file
                shutil.move(('D:/TempAudFiles/' + fileName.lower()), "D:\AudFiles")
            downloaded_temp = os.listdir("D:\TempAudFiles")
            for file in downloaded_temp:
                os.remove(file)                                     # Clean the remporary file, as some file failed to be downloaded and lay as dumpt file
    try:
        with open(file_directory, 'rb') as audioFiles:
            blob.upload_from_file(audioFiles, content_type='audio/mpeg')        # Save the audio to the firebase data storage
    except Exception as e:
        print('Audio {} was not saved to storage: '.format(fileName) + ': ' + e)
