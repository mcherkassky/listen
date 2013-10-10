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
        video_id = re.findall('[^/]+$', entry.id.text)[0]
        duration = entry.media.duration.seconds
        feed_out.append({'video_id': video_id,
                         'duration': duration})
    return feed_out