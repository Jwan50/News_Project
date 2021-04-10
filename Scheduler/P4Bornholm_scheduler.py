import schedule
import time
from radio_scrapers.p4_Bornholm_radio import scrap_P4_bornholm
scrape_back_days = 0
runType = 2

def run_P4_Bornholm():
    try:
        print('P4 Bornholm is running every 10 seconds ... ')
        scrap_P4_bornholm(scrape_back_days, runType)         # parameters: 1 scrap_back_days, 1 runType

    except Exception as e:
        print('Problem running P4 Bornholm scheduler: ', e)


schedule.every(10).seconds.do(run_P4_Bornholm)

while True:
    schedule.run_pending()
    time.sleep(1)
