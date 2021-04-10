import firebase
import firebase_admin
from firebase_admin import credentials, firestore, storage


def audio_to_Firestorage(fileName):
    cred = credentials.Certificate(
        "C:/Users\\gwan1\\PycharmProjects\\News_Project\\serviceAccountKey.json")
    firebase_admin.initialize_app(cred, {'storageBucket': 'the-news-project.appspot.com'})
    db = firestore.client()
    store = firebase.Storage()
    audios = store.list_files()

    for audio in audios:
        try:
            if audio:
                return
            else:
                bucket = storage.bucket()
                bucket.blob()
                file_dir = str("D:\\AudFiles" + '\\' + audio)
                blob = bucket.blob(audio)
                with open(file_dir, 'rb') as audioFiles:
                    blob.upload_from_file(audioFiles, content_type='audio/mpeg')
        except Exception as e:
            print(e)


try:
    audio_to_Firestorage()
except Exception as e:
    print(e)

    # dir = "D:\AudFiles"
    # downloaded = os.listdir(dir)
    #
    # for audio in downloaded:
    #     try:
