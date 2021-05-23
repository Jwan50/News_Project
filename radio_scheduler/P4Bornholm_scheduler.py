import schedule
import time
from radio_builder import p4_Bornholm_building

scrape_back_days = 0
runType = 2


class P4_bornholm:
    def __init__(self):
        self.runType = 2
        self.scrape_back_days = 2

    def run_P4_Bornholm(self):
        try:
            print('P4 Bornholm is running every 10 seconds ... ')
            p4 = p4_Bornholm_building.p4_bornholm_building(self.scrape_back_days, self.runType)
            p4.getRadio_p4()

        except Exception as e:
            print('Problem running P4 Bornholm scheduler: ', e)

    schedule.every(10).seconds.do(run_P4_Bornholm)


while True:
    sched_p4 = P4_bornholm()
    try:
        sched_p4.run_P4_Bornholm()
        schedule.run_pending()
        time.sleep(1)
    except Exception as e:
        print(e)
