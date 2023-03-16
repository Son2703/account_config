from base import *
import pymongo

Mongo_Client = pymongo.MongoClient(
    "mongodb://localhost:27017/", username= MONGO_USERNAME, password=MONGO_PASSWORD)


import redis

Redis_Client = redis.StrictRedis(host=REDIS_PORT, port=REDIS_PORT)
