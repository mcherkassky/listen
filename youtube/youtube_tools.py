__author__ = 'mcherkassky'
import re

from gdata.youtube import service

client = service.YouTubeService()
client.email = 'mcherkassky@gmail.com'
client.password = 'mAbel1127'
client.source = 'my-example-app'
client.ProgrammaticLogin()


#get video feed from search query
def getVideoFeed(search_text):
    query = service.YouTubeVideoQuery()
    query.vq = search_text
    query.orderby = 'relevance'
    query.max_results = 5
    query.racy = 'include' #query.racy
    feed = client.YouTubeQuery(query)

    feed_out = []
    for entry in feed.entry:
        title = entry.title.text
        img = entry.media.thumbnail[0].url
        youtube_url = re.findall('[^/]+$', entry.id.text)[0]
        try:
            view_count = entry.statistics.view_count
        except:
            view_count = ""
        author = entry.author[0].name.text
        duration = entry.media.duration.seconds
        try:
            description = entry.media.description.text[0:50] + '...'
        except:
            description = "No description available"
        feed_out.append({'title': title,
                         'img': img,
                         'view_count': view_count,
                         'author': author,
                         'youtube_url': youtube_url,
                         'artist': 'YouTube',
                         'duration': duration,
                         'description': description})
    return feed_out

#get actual youtube objects from feed
def getVideoObjects(search_text):
    query = service.YouTubeVideoQuery()
    query.vq = search_text
    query.orderby = 'relevance'
    query.max_results = 5
    query.racy = 'include' #query.racy
    feed = client.YouTubeQuery(query)

    out = [entry for entry in feed.entry]
    return out