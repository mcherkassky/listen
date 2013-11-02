from flask.ext.script import Manager, Shell

from youtube import app
from youtube import models
from random import randint

manager = Manager(app)

def _make_context():
	return {'app': app, 'models': models}

@manager.command
def hello():
	print "hello"


@manager.command
def get_echo_nest():
    import mongoengine
    from youtube.models import Song
    import random

    songs = Song.objects.limit(10)
    length = len(songs)

    randoms = [random.randint(0, length) for i in range(0, 100)]
    f = open('songnames.txt', 'w')
    for index, my_random in enumerate(randoms):
        print songs[my_random].title
        f.write(songs[my_random].title + '\n')
    f.close()

@manager.command
def artists():
    from youtube.models import *
    from settings import *
    import requests 

    songs = Song.objects.filter(artist="Daft Punk")
    print len(songs)
    print songs
    for song in songs:
        echo_response = requests.get("http://developer.echonest.com/api/v4/song/search?api_key={0}&format=json&results=1&artist={1}&title={2}".format(ECHONEST_API_KEY, song.artist, song.title))
        print echo_response


@manager.command
def make_echo_nest():
    from settings import *
    from youtube.models import Song
    import requests
    import random
    from StringIO import StringIO
    import json
    import time

    f = open('notalone.txt')
    lines = f.readlines()
    f.close()

    length = len(lines)

    for line in lines:
        random_song = line.split('<SEP>')
        print random_song
        song_id = random_song[0]
        song_artist = random_song[2]
        song_name = random_song[3]

        echo_response = requests.get("http://developer.echonest.com/api/v4/track/profile?api_key={0}&format=json&id={1}&bucket=title".format(ECHONEST_API_KEY, song_id))
        print echo_response.text
        import pdb; pdb.set_trace()

        io = StringIO(echo_response.text)
        song = json.load(io)
        try: 
            new_song = Song(

                    title=song_name,
                    artist=song_artist,
                    echo_nest_id = song_id,
                    time_signature = song['response']['track']['audio_summary']['time_signature'],
                    tempo = song['response']['track']['audio_summary']['tempo'],
                    energy = song['response']['track']['audio_summary']['energy'],
                    liveness = song['response']['track']['audio_summary']['liveness'],
                    speechiness = song['response']['track']['audio_summary']['speechiness'],
                    acousticness = song['response']['track']['audio_summary']['acousticness'],
                    danceability = song['response']['track']['audio_summary']['danceability'],
                    key = song['response']['track']['audio_summary']['key'],
                    duration = song['response']['track']['audio_summary']['duration'],
                    loudness = song['response']['track']['audio_summary']['loudness'],
                    valence = song['response']['track']['audio_summary']['valence'],
                    mode = song['response']['track']['audio_summary']['mode']
                )
            new_song.save()
        except:
            pass


        print echo_response.text
        time.sleep(1)




if __name__ == "__main__":
	manager.add_command('shell', Shell(make_context=_make_context))
	manager.run()




