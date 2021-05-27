

def p3_getDate(song, soup, today, link_url, linkName):
    if song.find('time') is None:
        return
    hm = song.find('time').text
    hm_nat = float(hm.replace(':', '.'))
    played_h_m = hm.split(':')
    played_h = played_h_m[0]
    played_m = played_h_m[1]

    if soup.find('div', {
        'class': 'playlist-program-details'}):  # because of p3 2021/02/ 09 and 10 natradio issue fixed
        nat = soup.find('div', {'class': 'playlist-program-details'}).text.strip()
        nat = nat.lower()
        if 'i dag' not in nat:
            day = nat[4:6]
            dt = today.replace(day=int(day), hour=int(played_h), minute=int(played_m), second=0,
                               microsecond=0)
        if 00.00 < hm_nat < 05.00 and 'i dag' in nat:
            _day = str(link_url).split('playlister/' + linkName + '/')[1]
            _day = _day[8:10]
            dt = today.replace(day=int(_day), hour=int(played_h), minute=int(played_m), second=0,
                               microsecond=0)
        if 05.00 < hm_nat < 24.00 and 'i dag' in nat:
            _day = str(link_url).split('playlister/' + linkName + '/')[1]
            _day = _day[8:10]
            dt = today.replace(day=int(_day), hour=int(played_h), minute=int(played_m), second=0,
                               microsecond=0)
    else:
        dt = today.replace(hour=int(played_h), minute=int(played_m), second=0, microsecond=0)

    return dt