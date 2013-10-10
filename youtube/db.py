from settings import *
import mongoengine

def connect():
	mongoengine.connect(MONGO_DATABASE_NAME, host=MONGO_HOST, port=MONGO_PORT, username=MONGO_USERNAME, password=MONGO_PASSWORD)

connect()
