__author__ = 'mcherkassky'

import datetime

from youtube import db
from mongoengine import *


class Playlist(EmbeddedDocument):

    user_id = ObjectIdField()
    name = StringField()
    songs = ListField(ObjectIdField)

    tags = ListField(StringField)


class User(Document):

    name = StringField()
    email = EmailField()
    playlist_ids = ListField(ObjectIdField())


    @property
    def playlists(self):
        playlists = Playlist.objects.filter(email=self.email)
        return playlists.to_json()


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
