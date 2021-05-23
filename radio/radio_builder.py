from radio import radio_object


class Radio_builder:
    def __init__(self, radio=radio_object.radio_object):
        self.radio = radio

    def setArtist(self, artist):
        self.radio.artist = artist
        return self

    def setTitle(self, title):
        self.radio.title = title
        return self

    def setFileName(self, fileName):
        self.radio.fileName = fileName
        return self

    def setDate(self, date):
        self.radio.date = date
        return self

    def build(self):
        return self.radio