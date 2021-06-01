import datetime


def berlingske_getDate(header, scrap_date):
    header_date = header.find('span', {'class': 'text-uppercase font-s2'}).text.lower()   # Tag where date is located
    if 'i går' in header_date.lower() or '/' in header_date:                              # If yesturday 'i går' or having /
        dt = scrap_date - datetime.timedelta(days=1)                                      # Today's date minus 1 day
        dt = dt.strftime('%Y-%m-%d')                                                      # Format the date string as Y - m - d only

    else:
        hm = header_date.split(':')
        h = int(hm[0])
        m = int(hm[1])
        dt = scrap_date.replace(hour=h, minute=m, second=0, microsecond=0)
        dt = dt.strftime('%Y-%m-%d')                                # Format the date string as Y - m - d only
    dt = datetime.datetime.strptime(dt, '%Y-%m-%d')                 # Convert the above string to datetime format
    return dt
