

def berlingske_getHeadline(header):
    headline = header.find('h4', {'class': 'teaser__title d-inline-block font-s4'}).text.strip()        # h4 tage with class name to get the headline
    return headline
