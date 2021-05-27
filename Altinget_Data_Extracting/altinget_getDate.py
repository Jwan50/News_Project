import datetime

months = {'januar': 1, 'februar': 2, 'marts': 3, 'april': 4, 'maj': 5, 'juni': 6, 'juli': 7, 'august': 8,
          'september': 9, 'oktober': 10, 'november': 11, 'december': 12}


def altinget_getDate(header, scrap_date):

    content_date = header.find('time').text
    content_date = content_date.split('.')
    day = content_date[0]
    year = content_date[1][-4:]
    content_month_danish = content_date[1][:-4].strip().lower()
    dt = ''
    for month_danish in months:
        if content_month_danish == month_danish:
            month = str(months[content_month_danish])
            dt = scrap_date.replace(day=int(day), month=int(month), year=int(year))
            dt = dt.strftime('%Y-%m-%d')
            dt = datetime.datetime.strptime(dt, '%Y-%m-%d')
            return dt
