

def p4_getDate(song, soup, today, link_url, linkName):
    hm = song.find('time').text
    hm_nat = float(hm.replace(':', '.'))            # initiating float value of hm of night time to be compared after
    played_h_m = hm.split(':')                      # Splitting to separate h and m
    played_h = played_h_m[0]                        # First index for h
    played_m = played_h_m[1]                        # Secodn index for m

    if soup.find('div', {                           # Below if statements are to fix the issue of getting different time value based on time of day
        'class': 'playlist-program-details'}):      # because of p3 2021/02/ 09 and 10 natradio issue fixed.
        nat = soup.find('div', {'class': 'playlist-program-details'}).text.strip()
        nat = nat.lower()
        if 'i dag' not in nat and 'P4 BORNHOLM'.lower() in nat:
            day = nat[13:15]
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