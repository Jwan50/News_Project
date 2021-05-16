import firebase_admin
from firebase_admin import credentials, firestore, storage


class save_audio_p3:
    def __init__(self, fileName, file_directory):
        self.fileName = fileName
        self.file_directory = file_directory

    def save_audio(self):
        if not len(firebase_admin._apps):
            cred = credentials.Certificate(r"C:\Users\gwan1\PycharmProjects\News_Project\serviceAccountKey.json")
            firebase_admin.initialize_app(cred)
        firestore.client()
        bucket = storage.bucket()
        blob = bucket.blob(self.fileName)
        try:
            with open(self.file_directory, 'rb') as audioFiles:
                blob.upload_from_file(audioFiles, content_type='audio/mpeg')
        except Exception as e:
            print('Audio {} was not saved to storage: '.format(self.fileName) + ': ' + str(e))

