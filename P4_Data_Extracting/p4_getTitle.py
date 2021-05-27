removing_word = {'(Radio Edit)', '(Remix)', '(Edit)', '(Single Edit)',
                 '(Boogie Edit)', '(No Rap Edit)', '(Studio 2054 Remix)',
                 '(Radio Version)', '(Gettic Remix)', '(Metro Mix)', '?//'}


def p4_getTitle(song):
    if song.find('a').text.strip():  # to insure that title exists
        title = song.find('a').text.strip()
    else:
        return

    if "'" in title:
        title = title.replace("'", ' ')

    for word in removing_word:
        title = title.replace(word, '')

    return title
