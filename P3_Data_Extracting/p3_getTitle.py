removing_word = {'(Radio Edit)', '(Remix)', '(Edit)', '?//'}

def p3_getTitle(song):
    if song.find('a').text.strip():  # to insure that title exists
        title = song.find('a').text.strip()
    else:
        return


    if "'" in title:  # to avoid conflict with sql quote
        title = title.replace("'", ' ')

    for word in removing_word:
        title = title.replace(word, '')

    return title