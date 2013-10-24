__author__ = 'mcherkassky'

import pdb
import json
import re
from bson import ObjectId

from auth import requires_auth
from youtube_tools import getVideoFeed, getVideoObjects
from flask import Flask, url_for, request, session, redirect, render_template, g
from mongoengine import *
from unidecode import unidecode
from models import Artist, Album, Song, Playlist, User
from youtube import app
from auth import requires_auth

def make_response(songs, album):
    response = [{
            'title': song.title,
            'artist': song.artist,
            'album': album.title,
            'img': album.img,
            'duration': song.duration,
            'youtube_url': song.youtube_url,
            'album_id': str(song.album_id),
            'artist_id': str(song.artist_id)
        } for song in songs]
    return json.dumps(response)

@app.route('/albums/<album_id>', methods=['GET'])
def albums(album_id):
    album = Album.objects.get(id=album_id)
    songs = [Song.objects.get(id=song_id) for song_id in album.songs]
    return make_response(songs, album)
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
    # songs = list(Song.objects(Q(title__icontains=query) | Q(album__icontains=query) | Q(artist__icontains=query)).order_by('listeners'))

    songs = list(Song.objects(Q(title__icontains=query) | Q(album__icontains=query) | Q(artist__icontains=query)).order_by('-listeners')[:20]) #fix this
    albums = list(Album.objects.order_by('-listeners').filter(Q(title__icontains=query) | Q(artist__icontains=query))[:25])
    artists = list(Artist.objects.order_by('-listeners').filter(name__icontains=query)[:5])

    #make response
    response = {
        'songs': [{
            'title': song.title,
            'artist': song.artist,
            'album': song.album,
            'img': song.img,
            'id': str(song.id),
            'album_index': song.album_index,
            'duration': song.duration,
            'youtube_url': song.youtube_url,
            'album_id': str(song.album_id),
            'artist_id': str(song.artist_id)
        } for song in songs],
        'albums': [{
            'title': album.title,
            'artist': album.artist,
            'img': album.img,
            'id': str(album.id)
        } for album in albums],
        'artists': [{
            'name': artist.name,
            'img': artist.img,
            'id': str(artist.id)
        } for artist in artists]
    }
    return json.dumps(response)

@app.route('/find/title/<title>/album/<album>/artist/<artist>/duration/<duration>', methods=['GET'])
def find(title, album, artist, duration):
    artist = artist.split(' feat. ')[0].split(' ft. ')[0].strip()
    title = re.sub("(?s)\(.*?Explicit.*?\)", '', title, flags=re.I)
    try:
        videoFeed = getVideoFeed(' '.join([title, artist]))
    except:
        videoFeed = getVideoFeed(unidecode(' '.join([title, artist])))
    range_bottom = int(duration) - 15
    range_top = int(duration) + 15

    matchingVideos = [video for video in videoFeed if range_bottom <= int(video['duration']) <= range_top]

    if not matchingVideos:
        response = videoFeed[0]['youtube_url']
    else:
        response = matchingVideos[0]['youtube_url']

    return response

@app.route('/find/<query>')
def youtube_find(query):
    try:
        videoFeed = getVideoFeed(query)
    except:
        videoFeed = getVideoFeed(unidecode(query))

    return json.dumps(videoFeed)

@app.route('/user/<user_id>/playlist', methods=['GET', 'POST'])
def playlist(user_id):
    if request.method == 'GET':
        playlists = Playlist.objects().filter(user_id=user_id)
        return playlists.to_json()
    if request.method == 'POST':
        playlist = Playlist()
        playlist.user_id = user_id
        playlist.name = 'New Playlist'
        playlist.song_ids = []
        playlist.save()
        return playlist.to_json()

@app.route('/user/<user_id>/playlist/<playlist_id>', methods=['GET','POST'])
def playlists(user_id, playlist_id):
    if request.method == 'GET':
        playlist = Playlist.objects.get(id=playlist_id)
        return playlist.to_json()
    if request.method == 'POST':
        data = request.json
        playlist = Playlist.objects.get(id=data['id'])
        playlist.song_ids = [ObjectId(song_id) for song_id in data['song_ids']]
        playlist.save()
        return 'success'

@app.route('/user/<user_id>/playlist/<playlist_id>/song', methods=['GET'])
def song_to_playlist(user_id, playlist_id):
    playlist = Playlist.objects.get(id=playlist_id)
    songs = [Song.objects.get(id=song_id).serialize for song_id in playlist.song_ids]
    return json.dumps(songs)

@app.route('/song/<song_id>', methods=['GET'])
def song(song_id):
    song = Song.objects.get(id=song_id)
    return json.dumps(song.serialize)

@app.route('/user', methods=['GET'])
def user():
    user = User.objects().first()
    return user.to_json()

@app.route('/artists/batch', methods=['POST'])
def artists_batch():
    data = request.json #artist ids
    albums = []
    for artist_id in data:
        artist = Artist.objects.get(id=artist_id)
        albums.append(artist.get_albums())
    return json.dumps(albums)



