import feedparser

rss_feeds = open('feeds.txt').readlines()

for rss_feed in rss_feeds:

    d = feedparser.parse(rss_feed)
    print(d['feed']['title'])
    print(d['feed']['link'])
    print(d.feed.subtitle)

    for post in d.entries:
        print("[" + post.updated + "] " + post.title + " <" + post.link + ">")
