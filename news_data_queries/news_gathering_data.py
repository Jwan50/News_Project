from news_data_queries.if_news_exist import is_news_exist
from news_data_queries.app_init_news import is_app_init_news


def news_gothering_data(headline, content, dt, provider, category, runType, data_name):
    if runType > 1:
        try:
            is_app_init_news()
            if is_app_init_news:
                is_news_exist(headline, content, dt, provider, category, data_name)
        except Exception as e:
            print(e)