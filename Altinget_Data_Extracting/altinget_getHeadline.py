

def altinget_getHeadline(header):

    headline = header.find('h3', {'class': 'media-heading media-heading-article'}).text.strip()     # h3 tage with class name to get the headline
    return headline
