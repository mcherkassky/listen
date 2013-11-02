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
    unicode = StringField()
    itunes_id = IntField()
    name = StringField()
    img = StringField()
    tags = ListField()
    similar = ListField()

    #stats
    plays = IntField()
    listeners = IntField()

    def get_albums(self):
        albums = [album.serialize for album in Album.objects.order_by('-listeners').filter(artist_id=self.id)[:15]]
        return albums

    @classmethod
    def get_popular(cls):
        popular = cls.objects.order_by('-listeners')[:15]
        return popular

    @property
    def serialize(self):
        response = {
            'id': str(self.id),
            'name': self.name,
            'img': self.img,
            'listeners': self.listeners,
            'plays': self.plays,
            'tags': self.tags
        }
        return response


class Album(Document):
    created_at = DateTimeField(default=datetime.datetime.now, required=True)

    ########hierarchy#########
    artist_id = ObjectIdField()
    ##########################
    title = StringField()
    artist = StringField()
    img = StringField()
    unicode = StringField()
    itunes_id = IntField()
    songs = ListField()

    tags = ListField()
    similar = ListField()

    #stats
    plays = IntField()
    listeners = IntField()

    @classmethod
    def get_popular(cls):
        popular = cls.objects.order_by('-listeners')[:15]
        return popular

    @property
    def serialize(self):
        response = {
            'id': str(self.id),
            'artist_id': str(self.artist_id),
            'title': self.title,
            'artist': self.artist,
            'img': self.img,
            'listeners': self.listeners
        }
        return response


class AudioSummary(EmbeddedDocument):
    """Echo Nest audio summary object, stuff we get back 
    when we query the features on the track.
    """

    echo_nest_id = StringField()
    time_signature = FloatField()
    tempo = FloatField()
    energy = FloatField()
    liveness = FloatField()
    speechiness = FloatField()
    acousticness = FloatField()
    danceability = FloatField()
    key = FloatField()
    duration = FloatField()
    loudness = FloatField()
    valence = FloatField()
    mode = FloatField()

    @classmethod
    def build_from_echo_response(self, result_song):
        audio_summary = AudioSummary()
        audio_summary.echo_nest_id=result_song.id
        audio_summary.tempo=result_song.audio_summary['tempo']
        audio_summary.energy=result_song.audio_summary['energy']
        audio_summary.liveness=result_song.audio_summary['liveness']
        audio_summary.speechiness=result_song.audio_summary['speechiness']
        audio_summary.acousticness=result_song.audio_summary['acousticness']
        audio_summary.danceability=result_song.audio_summary['danceability']
        audio_summary.key=result_song.audio_summary['key']
        audio_summary.duration=result_song.audio_summary['duration']
        audio_summary.loudness=result_song.audio_summary['loudness']
        audio_summary.valence=result_song.audio_summary['valence']
        audio_summary.mode=result_song.audio_summary['mode']
        return audio_summary


class Song(Document):
    created_at = DateTimeField(default=datetime.datetime.now, required=True)

    ########hierarchy#########
    artist_id = ObjectIdField()
    album_id = ObjectIdField()
    ##########################

    title = StringField()
    album = StringField()
    img = StringField()
    unicode = StringField()
    itunes_id = IntField()
    album_index = IntField()
    artist = StringField()

    duration = IntField()
    listeners = IntField()

    youtube_url = StringField()
    tag = StringField()

    audio_summary = EmbeddedDocumentField(AudioSummary)
    echo_nest_updated = BooleanField(default=False)



    @property
    def serialize(self):
        response = {
            'id': str(self.id),
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




