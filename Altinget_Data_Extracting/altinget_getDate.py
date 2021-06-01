import datetime

months = {'januar': 1, 'februar': 2, 'marts': 3, 'april': 4, 'maj': 5, 'juni': 6, 'juli': 7, 'august': 8,
          'september': 9, 'oktober': 10, 'november': 11, 'december': 12}   # list of months name in danish to compare, and number of the month


def altinget_getDate(header, scrap_date):

    content_date = header.find('time').text                             # Targeting 'time' child of header to get date string
    content_date = content_date.split('.')                              # As date comes in h.t.m format, need to be splitted to extract h and m separately
    day = content_date[0]                                               # Extracting day value from the string
    year = content_date[1][-4:]                                         # Extracting year value from the string
    content_month_danish = content_date[1][:-4].strip().lower()         # Extracting danish month value from the string

    for month_danish in months:                                         # Starting to compare danish and English months
        if content_month_danish == month_danish:
            month = str(months[content_month_danish])
            dt = scrap_date.replace(day=int(day), month=int(month), year=int(year))
            dt = dt.strftime('%Y-%m-%d')                                # Format the date string as Y - m - d only
            dt = datetime.datetime.strptime(dt, '%Y-%m-%d')             # Convert the above string to datetime format
            return dt
