import schedule
import time

from news_builder.altinget_building import alt_concretenews_building


class altinget_scheduler:
    def __init__(self):
        self.runType = 2

    def run_altinget(self):
        try:
            print('Altinget is running every 20 seconds ... ')
            altin = alt_concretenews_building(self.runType)
            altin.getNews_altinget()

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
