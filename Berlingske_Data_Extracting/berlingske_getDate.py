import datetime

months = {'januar': 1, 'februar': 2, 'marts': 3, 'april': 4, 'maj': 5, 'juni': 6, 'juli': 7, 'august': 8,
          'september': 9, 'oktober': 10, 'november': 11, 'december': 12}


def berlingske_getDate(header, scrap_date):
    header_date = header.find('span', {'class': 'text-uppercase font-s2'}).text.lower()
    if 'i går' in header_date.lower() or '/' in header_date:
        return
    hm = header_date.split(':')
    h = int(hm[0])
    m = int(hm[1])
    dt = scrap_date.replace(hour=h, minute=m, second=0, microsecond=0)
    dt = dt.strftime('%Y-%m-%d')
    dt = datetime.datetime.strptime(dt, '%Y-%m-%d')
    return dt
