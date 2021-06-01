from firebase_admin import storage
from firebase_admin import firestore


def is_audio_exist(fileName):
    audioList = []
    firestore.client()                          # Initiating client server

    bucket = storage.bucket().list_blobs()      # To return the list of audio file (it have blob datatype in database)
    for audio in bucket:
        audio = audio.name
        audioList.append(audio)                 # To create the list of audio in the database
    if fileName in audioList:
        return False
    else:
        return True
