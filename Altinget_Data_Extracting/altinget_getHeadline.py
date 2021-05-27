

def altinget_getHeadline(header):

    headline = header.find('h3', {'class': 'media-heading media-heading-article'}).text.strip()
    return headline
