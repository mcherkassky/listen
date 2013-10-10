__author__ = 'mcherkassky'

import datetime

from youtube import db


class Artist(db.Document):
    created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
    name = db.StringField()
    img = db.StringField()
    tags = db.ListField()
    similar = db.ListField()

    #stats
    plays = db.IntField()
    listeners = db.IntField()


class Album(db.Document):
    created_at = db.DateTimeField(default=datetime.datetime.now, required=True)

    ########hierarchy#########
    #artist_id = db.ObjectIdField()
    ##########################
    title = db.StringField()
    artist = db.ReferenceField('Artist') #db.StringField()
    img = db.StringField()

    tags = db.ListField()
    similar = db.ListField()

    #stats
    plays = db.IntField()
    listeners = db.IntField()


class Song(db.Document):
    created_at = db.DateTimeField(default=datetime.datetime.now, required=True)

    ########hierarchy#########
    #artist_id = db.ObjectIdField()
    #album_id = db.ObjectIdField()
    ##########################

    title = db.StringField()
    album = db.ReferenceField('Album')#db.StringField()
    album_index = db.IntField()
    artist = db.ReferenceField('Artist')#db.StringField()

    duration = db.IntField()
    listeners = db.IntField()

    youtube_url = db.StringField()