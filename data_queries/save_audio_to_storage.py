import firebase_admin
from firebase_admin import credentials, firestore, storage


def save_audio(fileName, file_directory):
    if not len(firebase_admin._apps):
        cred = credentials.Certificate(r"C:\Users\gwan1\PycharmProjects\News_Project\serviceAccountKey.json")
        firebase_admin.initialize_app(cred)
    firestore.client()
    bucket = storage.bucket()
    blob = bucket.blob(fileName)
    with open(file_directory, 'rb') as audioFiles:
        blob.upload_from_file(audioFiles, content_type='audio/mpeg')


try:
    save_audio()
except Exception as e:
    print(e)
