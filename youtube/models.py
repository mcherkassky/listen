__author__ = 'mcherkassky'

import datetime

from youtube import db
from mongoengine import *


class Playlist(Document):
    user_id = ObjectIdField()
    name = StringField()
    song_ids = ListField(ObjectIdField)

    tags = ListField(StringField)


class User(Document):

    name = StringField()
    email = EmailField()
    playlist_ids = ListField(ObjectIdField())


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
