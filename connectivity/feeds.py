import feedparser

from connectivity.singleton_observable import SingletonObservable

rss_feeds = open('../connectivity/feeds.txt').readlines()


class NewsAPI(SingletonObservable):
    _instance = None

    def __init__(self):
        super().__init__(NewsAPI)

    @staticmethod
    def display_news():
        for rss_feed in rss_feeds:

            d = feedparser.parse(rss_feed)
            print(d['feed']['title'])
            print(d['feed']['link'])
            print(d.feed.subtitle)

            for post in d.entries:
                print("[" + post.updated + "] " + post.title + " <" + post.link + ">")

    def poll(self):
        return {'key': 'news'}
