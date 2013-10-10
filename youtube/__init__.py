__author__ = 'mcherkassky'

import pdb

from flask import Flask
from flask.ext.mongoengine import MongoEngine

import settings


app = Flask(__name__)

app.debug = True
app.secret_key = 'zefr'
app.config.from_object(settings)
db = MongoEngine(app)

from youtube import models

from youtube import views