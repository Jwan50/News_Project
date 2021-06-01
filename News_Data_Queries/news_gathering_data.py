from News_Data_Queries.news_exist import is_news_exist
from News_Data_Queries.app_init_news import is_app_init_news


def gather_data(headline, content, dt, category, runType, data_name):
    if runType > 1:
        try:
            is_app_init_news()                                                          # To initiate firebase application
            if is_app_init_news:
                is_news_exist(headline, content, dt, category, data_name)     # If app initiated, go to is_news_exist
        except Exception as e:
            print(e)