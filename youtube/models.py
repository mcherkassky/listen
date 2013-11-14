__author__ = 'mcherkassky'

import datetime

from youtube import db
from mongoengine import *

from bson import ObjectId

class Echo(Document):
    #echonest
    tempo = FloatField()
    energy = FloatField()
    liveness = FloatField()
    speechiness = FloatField()
    acousticness = FloatField()
    danceability = FloatField()
    loudness = FloatField()
    valence = FloatField()

    song_id = ObjectIdField()


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

    # echo = EmbeddedDocumentField(Echo)

    def similar(self, discovery):
        try:
            echo = Echo.objects.get(song_id=self.id)
            tempo_range = (echo.tempo - discovery, echo.tempo + discovery)
            liveness_range = (echo.liveness - discovery, echo.liveness + discovery)
            speechiness_range = (echo.speechiness - discovery, echo.speechiness + discovery)
            acousticness_range = (echo.acousticness - discovery, echo.acousticness + discovery)
            danceability_range = (echo.danceability - discovery, echo.danceability + discovery)
            loudness_range = (echo.loudness - discovery, echo.loudness + discovery)
            valence_range = (echo.valence - discovery, echo.valence + discovery)

            echo_similar = Echo.objects.filter(
                Q(tempo__gte=tempo_range[0]) & Q(tempo__lte=tempo_range[1]) &
                Q(liveness__gte=liveness_range[0]) & Q(liveness__lte=liveness_range[1]) &
                Q(speechiness__gte=speechiness_range[0]) & Q(speechiness__lte=speechiness_range[1]) &
                Q(acousticness__gte=acousticness_range[0]) & Q(acousticness__lte=acousticness_range[1]) &
                Q(danceability__gte=danceability_range[0]) & Q(danceability__lte=danceability_range[1]) &
                Q(loudness__gte=loudness_range[0]) & Q(loudness__lte=loudness_range[1]) &
                Q(valence__gte=valence_range[0]) & Q(valence__lte=valence_range[1])
            )

            results = [Song.objects.get(id=echo.song_id) for echo in echo_similar]

            return results

        except:
            return None
        if self.echo is None:
            return None
        else:
            echo = self.echo

            energy = FloatField()
            liveness = FloatField()
            speechiness = FloatField()
            acousticness = FloatField()
            danceability = FloatField()
            loudness = FloatField()
            valence = FloatField()


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
    email = StringField()


class Global(Document):
    n_tokens = IntField()




