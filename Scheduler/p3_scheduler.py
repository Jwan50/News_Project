import schedule
from Radio_Scrapers.p3_scraper import scrap_P3
scrape_back_days = 2
runType = 2
runEvery = 0


def run_P3():
    try:
        print('P3 is running every 10 {} seconds ... '.format(runEvery))
        scrap_P3(scrape_back_days, runType)  # parameters: 1 scrap_back_days, 1 runType
    except Exception as e:
        print('Problem running run_P3 scheduler: ', e)


schedule.every(runEvery).hours.do(run_P3)

while True:
    schedule.run_pending()
