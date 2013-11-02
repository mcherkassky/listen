from settings import *
import mongoengine

def connect():
	# return mongoengine.connect(MONGO_DATABASE_NAME, 
    #         host=MONGO_HOST, 
    #         port=MONGO_PORT, 
    #         username=MONGO_USERNAME, 
    #         password=MONGO_PASSWORD)
	return mongoengine.connect(NEW_MONGO_DATABASE_NAME, 
            host=NEW_MONGO_HOST, 
            port=NEW_MONGO_PORT, 
            username=NEW_MONGO_USERNAME, 
            password=NEW_MONGO_PASSWORD)



connection = connect()
