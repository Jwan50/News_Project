import schedule
from news_builder.altinget_building import alt_concretenews_building

runEvery = 3600


def run_altinget():
    runType = 2
    alt = alt_concretenews_building(runType)
    alt.getNews_altinget()
    print('Altinget is running every {} seconds ... '.format(runEvery))


schedule.every(runEvery).seconds.do(run_altinget)

while True:
    schedule.run_pending()
