import schedule
from radio_scrapers.p3_radio import scrap_P3

scrape_back_days = 2
runType = 2
runEvery = 20


def run_P3():
    try:
        print('P3 is running every 10 {} seconds ... '.format(runEvery))
        scrap_P3(scrape_back_days, runType)  # parameters: 1 scrap_back_days, 1 runType
    except Exception as e:
        print('Problem running run_P3 scheduler: ', e)


schedule.every(10).seconds.do(run_P3)

while True:
    schedule.run_pending()
