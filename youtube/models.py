__author__ = 'mcherkassky'

import datetime

from youtube import db
from mongoengine import *


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
    #artist_id = ObjectIdField()
    ##########################
    title = StringField()
    artist = ReferenceField('Artist') #StringField()
    img = StringField()

    tags = ListField()
    similar = ListField()

    #stats
    plays = IntField()
    listeners = IntField()


class Song(Document):
    created_at = DateTimeField(default=datetime.datetime.now, required=True)

    ########hierarchy#########
    #artist_id = ObjectIdField()
    #album_id = ObjectIdField()
    ##########################

    title = StringField()
    album = ReferenceField('Album')#StringField()
    album_index = IntField()
    artist = ReferenceField('Artist')#StringField()

    duration = IntField()
    listeners = IntField()

    youtube_url = StringField()
