__author__ = 'mcherkassky'

import pdb

from flask import Flask, url_for, request, session, redirect, render_template, g
from flask.ext.mongoengine import MongoEngine
from functools import wraps
import logging
import requests
import db
from models import User, Playlist



import settings


app = Flask(__name__)

app.debug = True
app.secret_key = 'zefr'
app.config.from_object(settings)

from youtube import models
from youtube import views
from auth import requires_auth
from flask_oauth import OAuth


oauth = OAuth()

facebook = oauth.remote_app('facebook',
    base_url='https://graph.facebook.com/',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
    consumer_key=settings.FACEBOOK_APP_ID,
    consumer_secret=settings.FACEBOOK_SECRET_KEY,
    request_token_params={'scope': 'email, user_birthday'}
)


@facebook.tokengetter
def get_facebook_token():
    return session.get('facebook_token')

def pop_login_session():
    session.pop('logged_in', None)
    session.pop('facebook_token', None)


@app.route('/facebook_login')
def facebook_login():
    return facebook.authorize(callback=url_for('facebook_authorized',\
                next=request.args.get('next'), _external=True))



@app.route("/facebook_authorized")
@facebook.authorized_handler
def facebook_authorized(resp):
    print resp
    next_url = request.args.get('next') or url_for('index')
    if resp is None or 'access_token' not in resp:
        return redirect(next_url)

    session['logged_in'] = True
    session['facebook_token'] = (resp['access_token'], '')

    return redirect(next_url)


@app.route('/logout')
def logout():
    pop_login_session()
    return redirect(url_for('home'))



def facebook_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        print session
        if 'logged_in' not in session or 'facebook_token' not in session:
            return facebook.authorize(callback=url_for('facebook_authorized',\
                        next=request.args.get('next'), _external=True))
        else:
            fb_response = requests.get('https://graph.facebook.com/me?access_token=' + session['facebook_token'][0])
            text = fb_response.text
            from StringIO import StringIO
            import json
            io = StringIO(text)
            js = json.load(io)
            email = js['email']
            session['email'] = email

            return f(*args, **kwargs)
    return decorator



@app.route('/')
@requires_auth
# @facebook_required
def index():
    # user = User.get_by_email(session['email'])
    #
    # if user is None:
    #     user = User(email=session['email'])
    #     user.save()

    # session['user_id'] = user.id
    # g.user = user

    # playlists = user.playlists

    return render_template('/index/index.html')
            # playlists=playlists)



@app.route('/home')
def home():
    return render_template('home.html')



@app.route('/playlist', methods=["PUT"])
def add_to_playlist():
    return "adding to playlist"


@app.route('/user/playlists/', methods=["POST"])
def create_playlist():
    playlist_json = request.json
    playlist = Playlist(request.json['name'])
    playlist.user_id = session['user_id']
    playlist.save()
    
    g.user.add_playlist(playlist)

    return ""

@app.route('/user/playlists/<playlist_id>', methods=["DELETE"])
def delete_playlist(playlist_id):

    g.user.remove_playlist(playlist_id)

    return ""

@app.route('/user/playlists/<playlist_id>', methods=["PUT"])
def edit_playlist(playlist_id):

    playlist_json = request.json
    song_id = request.json['song_id']

    playlist = Playlist.objects.get(id=playlist_id)
    playlist.song_ids.append(song_id)
    playlist.save()

    return ""





