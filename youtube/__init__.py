__author__ = 'mcherkassky'

import pdb

from flask import Flask, url_for, request, session, redirect, render_template
from flask.ext.mongoengine import MongoEngine
from functools import wraps
import logging
import db

import settings


app = Flask(__name__)

app.debug = True
app.secret_key = 'zefr'
app.config.from_object(settings)


from youtube import models

from youtube import views





from flask_oauth import OAuth


oauth = OAuth()

facebook = oauth.remote_app('facebook',
    base_url='https://graph.facebook.com/',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
    consumer_key="529423813793656",
    consumer_secret="e3535cd1ebc8d29b712fc853b670ff9e",
    request_token_params={'scope': 'email'}
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
            return f(*args, **kwargs)
    return decorator



@app.route('/')
@facebook_required
def index():
    return render_template('/index/index.html')


@app.route('/home')
def home():
    return render_template('home.html')


