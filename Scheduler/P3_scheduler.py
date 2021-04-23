import schedule
import time
from radio_scrapers.p3_radio import scrap_P3

scrape_back_days = 0
runType = 2


def run_P3():
    try:
        print('P3 is running every 10 seconds ... ')
        scrap_P3(scrape_back_days, runType)  # parameters: 1 scrap_back_days, 1 runType
    except Exception as e:
        print('Problem running run_P3 scheduler: ', e)


schedule.every(10).seconds.do(run_P3)

try:
    run_P3()
    schedule.run_pending()
    time.sleep(1)
except Exception as e:
    print(e)
