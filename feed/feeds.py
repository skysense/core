import feedparser

d = feedparser.parse('http://feeds.feedburner.com/Coindesk?format=rss')
# print(d)
print(d['feed']['title'])
print(d['feed']['link'])
print(d.feed.subtitle)

for post in d.entries:
    print("[" + post.published + "] " + post.title + " <" + post.link + ">")
