removing_word = {'(Radio Edit)', '(Remix)', '(Edit)', '?//'}


def p4_getArtist(song):
    if song.find('span', itemprop="byArtist").text:  # to insure that artist exists
        artist = song.find('span', itemprop="byArtist").text.strip()
    else:
        return

    if "'" in artist:  # to avoid conflict with sql quote
        artist = artist.replace("'", '')

    return artist
