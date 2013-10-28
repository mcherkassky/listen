__author__ = 'mcherkassky'

import os
import logging 


MONGODB_SETTINGS = {
    "DB": "music"
}

# MONGO_HOST = "widmore.mongohq.com"
# MONGO_DATABASE_NAME = "listen2"
# MONGO_PORT = 10000
MONGO_HOST = "paulo.mongohq.com"
MONGO_DATABASE_NAME = "listen"
MONGO_PORT = 10035

MONGO_USERNAME = "listen"
MONGO_PASSWORD = "listener"

FACEBOOK_APP_ID = os.environ.get('FACEBOOK_APP_ID', "529423813793656")
FACEBOOK_SECRET_KEY = os.environ.get('FACEBOOK_APP_SECRET', "e3535cd1ebc8d29b712fc853b670ff9e")

