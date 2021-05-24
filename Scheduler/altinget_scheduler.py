import schedule
from news_scraping.altinget import scrape_altinget

runEvery = 10
runType = 2


def run_altinget():
    try:
        print('Altinget is running every {} seconds ... '.format(runEvery))
        scrape_altinget(runType)

    except Exception as e:
        print('Problem running Altinget scheduler: ', e)


schedule.every(runEvery).seconds.do(run_altinget)

while True:
    schedule.run_pending()
