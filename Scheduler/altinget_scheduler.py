import schedule
import time
from news_scraping.altinget import scrape_altinget


class altinget_scheduler:

    def run_altinget(self):
        try:
            print('Altinget is running every 20 seconds ... ')
            scrape_altinget(2)

        except Exception as e:
            print('Problem running Altinget scheduler: ', e)

    schedule.every(10).seconds.do(run_altinget)

    while True:
        try:
            run_altinget()

            schedule.run_pending()
            time.sleep(1)
        except Exception as e:
            print(e)
