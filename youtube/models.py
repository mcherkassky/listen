__author__ = 'mcherkassky'

import datetime

from youtube import db
from mongoengine import *

from bson import ObjectId


class Playlist(Document):
    user_id = ObjectIdField()
    name = StringField()
    song_ids = ListField(ObjectIdField())

    tags = ListField(StringField)

    def add_song(self, song):
        self.song_ids.append(song.id)
        self.save()

    @property
    def serialize(self):
        response = {
            'user_id': str(self.user_id),
            'name': self.name,
            'song_ids': [str(oid) for oid in self.song_ids]
        }
        return response


class User(Document):

    name = StringField()
    email = EmailField()
    playlist_ids = ListField(ObjectIdField())

    username = StringField()
    password = StringField()


    @property
    def playlists(self):
        playlists = Playlist.objects.filter(email=self.email)
        return playlists.to_json()


    @property
    def add_playlist(self, playlist):
        playlist_ids.append(playlist.id)


    @property
    def remove_playlist(self, playlist_id):
        playlist_ids.remove(playlist_id)
        try:
            Playlist.objects.get(id=playlist_id).delete()
        except:
            return



    @property
    def delete_playlist(self, playlist_id):
        try:
            Playlist.objects.get(id=playlist_id).delete()
        except:
            return


    @classmethod
    def exists(cls, email):
        users = User.objects.filter(email=email)
        if any(users):
            return True
        else:
            return False


    @classmethod
    def get_by_email(cls, email):
        users = User.objects.filter(email=email)
        if any(users):
            return users[0]
        else:
            return None


class Artist(Document):
    created_at = DateTimeField(default=datetime.datetime.now, required=True)
    name = StringField()
    img = StringField()
    tags = ListField()
    similar = ListField()

    #stats
    plays = IntField()
    listeners = IntField()

    def get_albums(self):
        albums = [album.serialize for album in Album.objects.order_by('-listeners').filter(artist_id = self.id)[:15]]
        return albums


class Album(Document):
    created_at = DateTimeField(default=datetime.datetime.now, required=True)

    ########hierarchy#########
    artist_id = ObjectIdField()
    ##########################
    title = StringField()
    artist = StringField()
    img = StringField()

    songs = ListField()

    tags = ListField()
    similar = ListField()

    #stats
    plays = IntField()
    listeners = IntField()

    @property
    def serialize(self):
        response = {
            'artist_id': str(self.artist_id),
            'title': self.title,
            'artist': self.artist,
            'img': self.img,
        }
        return response


class Song(Document):
    created_at = DateTimeField(default=datetime.datetime.now, required=True)

    ########hierarchy#########
    artist_id = ObjectIdField()
    album_id = ObjectIdField()
    ##########################

    title = StringField()
    album = StringField()
    img = StringField()

    album_index = IntField()
    artist = StringField()

    duration = IntField()
    listeners = IntField()

    youtube_url = StringField()

    @property
    def serialize(self):
        response = {
            'artist_id': str(self.artist_id),
            'album_id': str(self.album_id),
            'title': self.title,
            'album': self.album,
            'img': self.img,
            'artist': self.artist,
            'duration': self.duration,
            'youtube_url': self.youtube_url
        }
        return response



class Token(Document):
    key = StringField()
    used = BooleanField(default=False)


class Global(Document):
    n_tokens = IntField()




