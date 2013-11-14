import urllib2
import pdb
import lxml
import re
import time
from unidecode import unidecode

from youtube.models import Artist, Album, Song, Echo
from bs4 import BeautifulSoup

from pyechonest import config
from pyechonest import song as pysong
from time import sleep

config.ECHO_NEST_API_KEY="KAPIZ5M8F1XNTSG85"
from mongoengine import Q
import pytunes as pytunes
import pylast

LASTFM_URL = 'http://www.last.fm/music/'
API_KEY = "bb8797676af1bedf371e8958650a2f1a"
API_SECRET = "22c9a6ca1720eb152af57b02c9f304a2"
username = "mcherkassky"
password_hash = pylast.md5("mike112791")
network = pylast.LastFMNetwork(api_key=API_KEY, api_secret=API_SECRET, username=username, password_hash=password_hash)


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

    try:
        artistdb = Artist.objects.get(itunes_id=artistdb.itunes_id)
        continue
    except:

        artistdb.name = artist.get_name()
        artistdb.genre = artist.get_genre()
        artistdb.unicode = unidecode(artistdb.name)

        last_artist = network.get_artist(artistdb.name)
        artistdb.img = last_artist.get_cover_image()
        artistdb.tags = [tag.item.name for tag in last_artist.get_top_tags(limit=10)]
        try:
            artistdb.listeners = last_artist.get_listener_count()
        except:
            pass

        artistdb.save()

    for album in artist.get_albums():
        albumdb = Album()
        albumdb.title = album.get_name()
        albumdb.itunes_id = album.get_id()
        albumdb.songs = []
        try:
            albumdb = Album.objects.get(itunes_id=albumdb.itunes_id)
            continue
        except:

            albumdb.unicode = unidecode(albumdb.title)
            albumdb.artist_id = artistdb.id
            albumdb.artist = artistdb.name

            try:
                last_album = network.get_album(albumdb.artist, albumdb.title)
                albumdb.img = last_album.get_cover_image()
            except:
                pass
            try:
                albumdb.listeners = last_album.get_listener_count()
                albumdb.tags = [tag.name for tag in last_album.get_top_tags(limit=10)]
            except:
                pass

            albumdb.save()

        print albumdb.title
        try:
            tracks = album.get_tracks()
        except:
            continue
        for track in album.get_tracks():
            songdb = Song()
            songdb.artist_id = artistdb.id
            songdb.artist = albumdb.artist
            songdb.album_id = albumdb.id
            songdb.itunes_id = track.get_id()
            songdb.album_index = track.get_disc_number()
            songdb.title = track.get_name()
            songdb.unicode = unidecode(songdb.title)
            songdb.album = albumdb.title
            songdb.img = albumdb.img

            try:
                last_song = network.get_track(albumdb.artist, songdb.title)
                songdb.listeners = last_song.get_listener_count()
            except:
                pass
            try:
                songdb.duration = int(round(track.get_duration()))
            except:
                songdb.duration = 0

            try:
                songdb = Song.objects.get(itunes_id=songdb.itunes_id)
                continue
            except:
                try:
                    echo = pysong.search(artist=unidecode(songdb.artist), title=unidecode(songdb.title))[0]
                    audio_features = echo.audio_summary
                    sleep(.5)
                    echo_data = Echo(
                        tempo=audio_features['tempo'] / 500.0,
                        energy=audio_features['energy'],
                        liveness=audio_features['liveness'],
                        speechiness=audio_features['speechiness'],
                        acousticness=audio_features['acousticness'],
                        danceability=audio_features['danceability'],
                        loudness=(audio_features['loudness'] + 100.0)/100.0,
                        valence=audio_features['valence'],
                        song_id = songdb.id
                    )

                    echo_data.save()
                except:
                    pass
                songdb.save()
                albumdb.songs.append(songdb.id)
                albumdb.save()
