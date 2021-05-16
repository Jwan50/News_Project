import schedule
import time
from news_scraping import altinget


class altinget_scheduler:
    def __init__(self):
        self.runType = 2

    def run_altinget(self):
        try:
            print('Altinget is running every 20 seconds ... ')
            altig = altinget.Altinget(self.runType)
            altig.scrape_altinget()

        except Exception as e:
            print('Problem running Altinget scheduler: ', e)

    schedule.every(10).seconds.do(run_altinget)


while True:
    sched = altinget_scheduler()
    try:
        sched.run_altinget()
        schedule.run_pending()
        time.sleep(1)
    except Exception as e:
        print(e)
