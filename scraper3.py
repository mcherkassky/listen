import urllib2
import pdb
import lxml
import re
from unidecode import unidecode

from youtube.models import Artist, Album, Song
from bs4 import BeautifulSoup
LASTFM_URL = 'http://www.last.fm/music/'
from mongoengine import Q
import pytunes as pytunes

def open_artists(path):
    f = open(path, 'rb')
    artists = f.readlines()
    return artists

artists = open_artists('unique_artists.txt')

for a in artists:
    artist = pytunes.search_artist(a)[0]
    artistdb = Artist()
    print artist.get_name()
    artistdb.itunes_id = artist.get_id()
    artistdb.name = artist.get_name()
    artistdb.genre = artist.get_genre()
    artistdb.unicode = unidecode(artistdb.name)

    try:
        artistdb = Artist.objects.get(itunes_id = artistdb.itunes_id)
        continue
    except:
        artistdb.save()

    for album in artist.get_albums():
        albumdb = Album()
        albumdb.title = album.get_name()
        albumdb.itunes_id = album.get_id()
        albumdb.unicode = unidecode(albumdb.title)
        albumdb.artist_id = artistdb.id
        albumdb.img = album.get_artwork()['100']

        try:
            albumdb = Album.objects.get(itunes_id = albumdb.itunes_id)
            continue
        except:
            albumdb.save()

        print albumdb.title
        try:
            tracks = album.get_tracks()
        except:
            continue
        for track in album.get_tracks():
            songdb = Song()
            songdb.artist_id = artistdb.id
            songdb.album_id = albumdb.id
            songdb.itunes_id = track.get_id()
            songdb.album_index = track.get_disc_number()
            songdb.title = track.get_name()
            songdb.unicode = unidecode(songdb.title)
            try:
                songdb.duration = int(round(track.get_duration()))
            except:
                songdb.duration = 0

            try:
                songdb = Song.objects.get(itunes_id = songdb.itunes_id)
                continue
            except:
                songdb.save()
