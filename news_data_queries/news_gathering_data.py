from news_data_queries.news_exist import is_news_exist
from news_data_queries.app_init_news import is_app_init_news


def gather_data(headline, content, dt, provider, category, runType, data_name):
    if runType > 1:
        try:
            is_app_init_news()                                                          # To initiate firebase application
            if is_app_init_news:
                is_news_exist(headline, content, dt, provider, category, data_name)     # If app initiated, go to is_news_exist
        except Exception as e:
            print(e)