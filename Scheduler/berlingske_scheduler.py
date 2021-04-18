import schedule

import time

from news_scraping.berlingske import scrape_berlingske


def run_berlingski():
    try:
        print('Berlingski is running every 20 seconds ... ')
        scrape_berlingske(2)

    except Exception as e:
        print('Problem running Berlingski scheduler: ', e)


schedule.every(10).seconds.do(run_berlingski)

while True:
    try:
        run_berlingski()

        schedule.run_pending()
        time.sleep(1)
    except Exception as e:
        print(e)