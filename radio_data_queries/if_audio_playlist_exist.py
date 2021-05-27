from firebase_admin import firestore, storage
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from radio_data_queries.save_audio_to_storage import save_audio
from radio_data_queries.if_playlist_exist import is_playlist_exist
from radio_data_queries.playlist_saving import playlist_to_Fir


def is_audio_playlist_exist(artist, title, dt, data_name, runType, fileName, file_directory):
    audioList = []
    firestore.client()

    bucket = storage.bucket().list_blobs()
    for audio in bucket:
        audio = audio.name
        audioList.append(audio)
    if fileName not in audioList:
        save_audio(artist, title, fileName, file_directory)
        if save_audio:
            print('Audio: ', ' -', artist, ' -', title, ' -', dt, 'saved')

    if not len(firebase_admin._apps):
        cred = credentials.Certificate(r"C:\Users\gwan1\PycharmProjects\News_Project\serviceAccountKey.json")
        firebase_admin.initialize_app(cred)

    db = firestore.client()
    if not db.collection(data_name).where('date', '==', dt).where('title',
                                                                  '==', title).where('artist', '==', artist).get():
        playlist_to_Fir(title, artist, dt, fileName, data_name)
        if playlist_to_Fir:
            print('Playlist: ', ' -', artist, ' -', title, ' -', dt, 'saved')


    # if playlist_to_Fir and save_audio:
    #     print('playlist: ', ' -', artist, ' -', title, ' -', dt, 'saved')
