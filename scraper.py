__author__ = 'mcherkassky'

import urllib2
import pdb
import lxml
import re
from unidecode import unidecode

from youtube.models import Artist, Album, Song
from bs4 import BeautifulSoup
from mongoengine import Q
LASTFM_URL = 'http://www.last.fm/music'
def open_landing(url, counter=1):
    try:
        landing = BeautifulSoup(urllib2.urlopen(url).read(),'lxml')
        return landing
    except:
        print(counter)
        if counter == 3:
            return None
        counter += 1
        open_landing(url, counter)

def time_to_seconds(time):
    (minutes, seconds) = time.split(':')
    return int(minutes)*60 + int(seconds)

def scrape_album_landing_page(url, artist):
    while True:
        # try:
        landing = open_landing(url)
        if landing is None:
            continue

        try:
            links = [album.find('a').get('href') for album in landing.findAll('div', {'class', 'album-item-detail-wrapper'})]
            #scrape all album pages
            albums = [scrape_album_page('http://www.lastfm.com' + link, artist) for link in links]
        except:
            continue

        if None in albums:
            break

        try:
            url = 'http://www.lastfm.com' + landing.find('div', {'class', 'whittle-pagination'}).find('a', {'class', 'iconright'}).get('href')
        except:
            break




def scrape_album_page(url, artist):
    landing = open_landing(url)
    if landing is None:
        return None

    try:
        album_plays = landing.find('li', {'class','scrobbles'}).find('b').string.replace(',', '')
    except:
        return None

    if int(album_plays) < 10000:
        return None

    album_title = landing.find('div', {'class', 'crumb-wrapper'}).find('h1').string.strip()
    print album_title

    album_img = landing.find('div', {'class', 'album-cover-wrapper'}).find('img').get('src')
    try:
        album_listeners = landing.find('li', {'class', 'listeners'}).find('b').string.replace(',', '')
    except:
        album_listeners = ""

    album = Album(title=unidecode(album_title),
                  artist=unidecode(artist.name),
                  artist_id=artist.id,
                  songs=[],
                  img=album_img,
                  plays=album_plays,
                  listeners=album_listeners)

    album.save()
    try:
        songs = landing.find('table', id='albumTracklist').find('tbody').findAll('tr')
    except:
        return None

    for (i, song) in enumerate(songs):
        song_title = song.find('td', {'class', 'subjectCell'}).find('span').string
        try:
            song_duration = time_to_seconds(song.find('td', {'class', 'durationCell'}).string.strip())
        except:
            song_duration = time_to_seconds(re.findall('[0-9]*:[0-9]*', str(song.find('td', {'class', 'durationCell'})))[0])
            #song_duration = -1
        try:
            song_listeners = song.find('td', {'class', 'reachCell'}).string.strip().replace(',', '')
        except:
            song_listeners = "0"

        if int(song_listeners) < .05 * int(album_listeners):
            continue

        try:
            song = Song.objects().get(Q(title=unidecode(song_title)) & Q(artist=artist.name) & Q(duration=song_duration))
            album = Album.objects.get(id=album.id)
            album.songs.append(song.id)
            album.save()
        except:
            song = Song(title=unidecode(song_title),
                        artist=unidecode(artist.name),
                        artist_id=artist.id,
                        album=unidecode(album.title),
                        album_id=album.id,
                        img=album_img,
                        album_index=i,
                        duration=song_duration,
                        listeners=song_listeners)
            song.save()
            album = Album.objects.get(id=album.id)
            album.songs.append(song.id)
            album.save()
    return 'success'


def scrape_landing_page(url):

    landing = BeautifulSoup(urllib2.urlopen(url).read(), 'lxml')
    artist_list = landing.find('ul', {'class', 'artistList'}).findAll('li')

    for artist in artist_list:
        try:
            link = artist.find('a').get('href')

            img = artist.find('span', {'class', 'image'}).find('img').get('src')
            name = artist.find('strong', {'class', 'name'}).string
            f.write(name + '\n')

            continue
            tags = [tag.find('a').string for tag in landing.find('ul', {'class', 'tags'}).findAll('li')]
        except:
            continue
        print name
        try:
            similar_artists = [element.string for element in artist.find('p', {'class', 'similar'}).findAll('a')]
        except:
            similar_artists = []

        try:
            stats = re.findall(r'\d+', artist.find('p', {'class','stats'}).string.replace(',',''))
            plays = stats[0]
            listeners = stats[1]
        except:
            plays = ""
            listeners = ""
        artist_exist = Artist.objects().filter(name=unidecode(name))
        if len(artist_exist) > 0:
            continue

        artistdb = Artist(name=unidecode(name),
                          img=img,
                          similar=similar_artists,
                          plays=plays,
                          tags=tags,
                          listeners=listeners)
        artistdb.save()

        scrape_album_landing_page('http://www.lastfm.com' + link + '/+albums', artistdb)



#scrape_landing_page(LASTFM_URL)
# songs = Song.objects.all()
# [song.delete() for song in songs]
# albums = Album.objects.all()
# [album.delete() for album in albums]
# artists = Artist.objects.all()
# [artist.delete() for artist in artists]

f = open('out.txt', 'w')
for i in xrange(1, 101):
    print i
    scrape_landing_page('http://www.last.fm/music?page=' + str(i))
f.close()

