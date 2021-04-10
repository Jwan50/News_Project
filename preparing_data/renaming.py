import os


def renaming():
    dir = "D:\AudFiles"
    downloaded = os.listdir(dir)
    for audio in downloaded:
        reName = audio[:-3] + 'mp3'.lower()
        fro = str(dir + '/' + str(audio)).strip()
        to = str(dir + '/' + str(reName)).strip()
        os.rename(fro, to)


try:
    renaming()
except Exception as e:
    print(e)