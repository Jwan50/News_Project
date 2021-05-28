from radio_data_queries.app_init_radio import is_app_init_radio
from radio_data_queries.if_audio_exist import is_audio_exist
from radio_data_queries.if_playlist_exist import is_playlist_exist
from radio_data_queries.playlist_saving import playlist_to_Fir
from radio_data_queries.save_audio_to_storage import save_audio


def radio_gathering_data(artist, title, dt, runType, data_name):
    if runType > 1:
        if is_app_init_radio:
            audioName = artist + ' - ' + title + '.mp3'
            fileName = str(audioName.lower())
            file_directory = "D:\AudFiles" + "\\" + fileName
            fileName = str(audioName.lower())

            if is_audio_exist(artist, title, dt, data_name, runType, fileName, file_directory) and is_playlist_exist(
                    title, artist, dt, fileName, data_name):
                save_audio(artist, title, fileName, file_directory)
                if save_audio:
                    print('Audio: ', ' -', artist, ' -', title, ' -', dt, 'saved')
                else:
                    return

                playlist_to_Fir(title, artist, dt, fileName, data_name)
                if playlist_to_Fir:
                    print('Playlist: ', ' -', artist, ' -', title, ' -', dt, 'saved')
            if not is_audio_exist(artist, title, dt, data_name, runType, fileName, file_directory) and is_playlist_exist(
                    title, artist, dt, fileName, data_name):
                playlist_to_Fir(title, artist, dt, fileName, data_name)
                if playlist_to_Fir:
                    print('Playlist: ', ' -', artist, ' -', title, ' -', dt, 'saved')

            if is_audio_exist(artist, title, dt, data_name, runType, fileName,
                                  file_directory) and not is_playlist_exist(
                    title, artist, dt, fileName, data_name):
                save_audio(artist, title, fileName, file_directory)
                if save_audio:
                    print('Audio: ', ' -', artist, ' -', title, ' -', dt, 'saved')
        else:
            radio_gathering_data(artist, title, dt, runType, data_name)
