import schedule
import time
from radio_scrapers import p3_radio

class P3_scheduler:
    def __init__(self):
        self.runType = 2
        self.scrape_back_days = 2

    def run_P3(self):
        try:
            print('P3 is running every 10 seconds ... ')
            p3 = p3_radio.p3_radio(self.scrape_back_days, self.runType)
            p3.scrap_P3()
        except Exception as e:
            print('Problem running run_P3 scheduler: ', e)


    schedule.every(10).seconds.do(run_P3)
while True:
    sched_p3 = P3_scheduler()
    try:
        sched_p3.run_P3()
        schedule.run_pending()
        time.sleep(1)
    except Exception as e:
        print(e)
