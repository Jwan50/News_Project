import schedule
import time
from news_scraping import berlingske


class berlingske_scheduler:
    def __init__(self):
        self.runType = 2

    def run_berlingski(self):
        try:
            print('Berlingski is running every 10 seconds ... ')
            berl = berlingske.Berlingske(self.runType)
            berl.scrape_berlingske()

        except Exception as e:
            print('Problem running Berlingski scheduler: ', e)

    schedule.every(10).seconds.do(run_berlingski)


while True:
    sched = berlingske_scheduler()
    try:
        sched.run_berlingski()
        schedule.run_pending()
        time.sleep(1)
    except Exception as e:
        print(e)
