import schedule
from Radio_Scrapers.p4_scraper import scrap_P4

scrape_back_days = 2
runType = 2
runEvery = 0


def run_P4_Bornholm():
    try:
        print('P4 Bornholm is running every {} seconds ... '.format(runEvery))
        scrap_P4(scrape_back_days, runType)  # parameters: 1 scrap_back_days, 1 runType

    except Exception as e:
        print('Problem running P4 Bornholm scheduler: ', e)


schedule.every(runEvery).hours.do(run_P4_Bornholm)

while True:
    schedule.run_pending()
