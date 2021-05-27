from radio_data_queries.app_init_radio import is_app_init_radio
from radio_data_queries.if_audio_playlist_exist import is_audio_playlist_exist


def radio_gothering_data(artist, title, dt, runType, data_name):
    if runType > 1:
        is_app_init_radio()
        if is_app_init_radio:
            audioName = artist + ' - ' + title + '.mp3'
            fileName = str(audioName.lower())
            file_directory = "D:\AudFiles" + "\\" + fileName
            fileName = str(audioName.lower())
            is_audio_playlist_exist(artist, title, dt, data_name, runType, fileName, file_directory)
