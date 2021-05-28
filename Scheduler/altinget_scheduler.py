import schedule
from news_scraping.altinget import scrape_altinget

runEvery = 2
runType = 2  # runType is optional: 1 for only printing the scraper result, 2 for printing and saving the data to firebase


def run_altinget():
    try:
        print('Altinget is running every {} seconds ... '.format(runEvery))
        scrape_altinget(runType)

    except Exception as e:
        print('Problem running Altinget scheduler: ', e)


schedule.every(runEvery).hours.do(run_altinget)

while True:
    schedule.run_pending()
