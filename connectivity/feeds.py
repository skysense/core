import feedparser

from connectivity.observable import Observable

rss_feeds = open('../connectivity/feeds.txt').readlines()


class NewsAPI(Observable):
    def run_news(self):
        for rss_feed in rss_feeds:

            d = feedparser.parse(rss_feed)
            print(d['feed']['title'])
            print(d['feed']['link'])
            print(d.feed.subtitle)

            for post in d.entries:
                print("[" + post.updated + "] " + post.title + " <" + post.link + ">")

    def poll(self):
        return {'key': 'news'}
