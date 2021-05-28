from firebase_admin import firestore, storage
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

from radio_data_queries.if_playlist_exist import is_playlist_exist
from radio_data_queries.save_audio_to_storage import save_audio
from radio_data_queries.playlist_saving import playlist_to_Fir


def is_audio_exist(artist, title, dt, data_name, runType, fileName, file_directory):
    audioList = []
    firestore.client()

    bucket = storage.bucket().list_blobs()
    for audio in bucket:
        audio = audio.name
        audioList.append(audio)
    if fileName in audioList:
        return False
    else:
        return True
