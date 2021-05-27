import time

import schedule
from news_scraping.berlingske import scrape_berlingske

runEvery = 5
runType = 1  # runType is optional: 1 for only printing the scraper result, 2 for printing and saving the data to firebase


def run_berlingski():
    try:
        print('Berlingski is running every {} seconds ... '.format(runEvery))
        scrape_berlingske(runType)

    except Exception as e:
        print('Problem running Berlingski scheduler: ', e)


schedule.every(runEvery).seconds.do(run_berlingski)

while True:
    schedule.run_pending()
    time.sleep(1)
