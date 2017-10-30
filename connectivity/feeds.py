import feedparser

from connectivity.singleton_observable import SingletonObservable


class NewsAPI(SingletonObservable):
    _instance = None

    def __init__(self):
        super().__init__(NewsAPI)
        self.filename = '../connectivity/feeds.txt'

    def read_rss_feeds(self):
        if not os.path.isfile(self.filename):
            return {}  # non existing file.
        if os.stat(self.filename).st_size == 0:
            return {}  # empty file.
        else:
            rss_feeds = open(self.filename).readlines()
            return rss_feeds

    def run_news(self):
        rss_feeds = self.read_rss_feeds()
        for rss_feed in rss_feeds:

            d = feedparser.parse(rss_feed)
            print(d['feed']['title'])
            print(d['feed']['link'])
            print(d.feed.subtitle)

            for post in d.entries:
                print("[" + post.updated + "] " + post.title + " <" + post.link + ">")

    def poll(self):
        return {'key': 'news'}
