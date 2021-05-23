import schedule
import time
from news_builder.berlingske_building import  ber_concretenews_building


class berlingske_scheduler:
    def __init__(self):
        self.runType = 2

    def run_berlingski(self):
        try:
            print('Berlingski is running every 10 seconds ... ')
            ber = ber_concretenews_building(self.runType)
            ber.getNews_berlingske()

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
