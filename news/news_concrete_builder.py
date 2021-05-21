from news import news_object


class News_concrete_builder:
    def __init__(self, news=news_object.news_object()):
        self.news = news

    def setCategory(self, category):
        self.news.category = category
        return self

    def setHeadline(self, headline):
        self.news.headline = headline
        return self

    def setContent(self, content):
        self.news.content = content
        return self

    def setDate(self, date):
        self.news.date = date
        return self

    def setProvider(self, provider):
        self.news.provider = provider
        return self

    def build(self):
        return self.news