__author__ = 'mcherkassky'

import datetime

from youtube import db
from mongoengine import *


class Playlist(EmbeddedDocument):

    name = StringField()
    songs = ListField(ObjectIdField)



class User(Document):

    name = StringField()
    email = EmailField()
    playlists = ListField(EmbeddedDocumentField(Playlist))

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
