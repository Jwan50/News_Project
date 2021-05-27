import schedule
from news_builder.berlingske_building import ber_concretenews_building

runEvery = 3600


def run_berlingski():
    runType = 2
    ber = ber_concretenews_building(runType)
    ber.getNews_berlingske()
    print('Berlinske is running every {} seconds ... '.format(runEvery))


schedule.every(runEvery).seconds.do(run_berlingski)

while True:
    schedule.run_pending()
