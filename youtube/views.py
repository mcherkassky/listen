__author__ = 'mcherkassky'

import pdb
import json

from youtube_tools import getVideoFeed
from flask import render_template
from mongoengine import *
from unidecode import unidecode
from models import Artist, Album, Song
from youtube import app

def make_response(songs):
    response = [{
            'title': song.title,
            'artist': song.artist.name,
            'album': song.album.title,
            'img': song.album.img,
            'album_index': song.album_index,
            'duration': song.duration,
            'youtube_url': song.youtube_url,
            'album_id': str(song.album.id),
            'artist_id': str(song.artist.id)
        } for song in songs]
    return json.dumps(response)

@app.route('/')
def index():
    return render_template('/index/index.html')

@app.route('/albums/<album_id>', methods=['GET'])
def albums(album_id):
    album = Album.objects.get(id=album_id)
    songs = Song.objects.filter(album=album).order_by('album_index')
    return make_response(songs)
    #pdb.set_trace()

# @app.route('/songs')
# def songs(query=""):
#     return Song.objects.filter(title__icontains=query)

@app.route('/artists')
def artist():
    pass

@app.route('/search/<query>')
def search(query):
    query = query.replace('+', ' ')
    songs = list(Song.objects(Q(title__icontains=query)).order_by('-listeners')[:20]) #fix this
    # songs = list(Song.objects.order_by('-listeners').filter(title__icontains=query)[:20]) #fix this
    albums = list(Album.objects.order_by('-listeners').filter(title__icontains=query)[:5])
    artists = list(Artist.objects.order_by('-listeners').filter(name__icontains=query)[:5])


    #make response
    response = {
        'songs': [{
            'title': song.title,
            'artist': song.artist.name,
            'album': song.album.title,
            'img': song.album.img,
            'album_index': song.album_index,
            'duration': song.duration,
            'youtube_url': song.youtube_url,
            'album_id': str(song.album.id),
            'artist_id': str(song.artist.id)
        } for song in songs],
        'albums': [{
            'title': album.title,
            'artist': {
                'name': album.artist.name,
                'img': album.artist.img,
                'id': str(album.artist.id),
                'listeners': album.artist.listeners
            },
            'img': album.img,
            'id': str(album.id)
        } for album in albums],
        'artists': [{
            'name': artist.name,
            'img': artist.img,
            'id': str(artist.id)
        } for artist in artists],
    }
    # {
    #     'songs': [{
    #         'title': song.title,
    #         'artist': {
    #             'name': song.artist.name,
    #             'img': song.artist.img,
    #             'id': str(song.artist.id),
    #             'listeners': song.artist.listeners
    #         },
    #         'album': {
    #             'title': song.album.title,
    #             'img': song.album.img,
    #             'id': str(song.album.id),
    #             'listeners': song.album.listeners
    #         },
    #         'album_index': song.album_index,
    #         'duration': song.duration,
    #         'youtube_url': song.youtube_url
    #     } for song in songs],
    #     'albums': [{
    #         'title': album.title,
    #         'artist': {
    #             'name': album.artist.name,
    #             'img': album.artist.img,
    #             'id': str(album.artist.id),
    #             'listeners': album.artist.listeners
    #         },
    #         'img': album.img,
    #         'id': str(album.id)
    #     } for album in albums],
    #     'artists': [{
    #         'name': artist.name,
    #         'img': artist.img,
    #         'id': str(artist.id)
    #     } for artist in artists],
    # }
    return json.dumps(response)

@app.route('/find/title/<title>/album/<album>/artist/<artist>/duration/<duration>', methods=['GET'])
def find(title, album, artist, duration):
    try:
        videoFeed = getVideoFeed(' '.join([title, artist]))
    except:
        videoFeed = getVideoFeed(unidecode(' '.join([title, artist])))
    range_bottom = int(duration) - 15
    range_top = int(duration) + 15

    matchingVideos = [video for video in videoFeed if range_bottom <= int(video['duration']) <= range_top]

    if not matchingVideos:
        response = videoFeed[0]['video_id']
    else:
        response = matchingVideos[0]['video_id']

    return response



