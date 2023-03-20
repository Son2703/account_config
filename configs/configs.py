from configs.base import *
import pymongo

Mongo_Client = pymongo.MongoClient(
    host="config-account-mongo", port=27017, username=MONGO_USERNAME, password=MONGO_PASSWORD)

CONFIG_ACCOUNT_DB = Mongo_Client[MONGO_DB]


import redis

Redis_Client = redis.StrictRedis(host=REDIS_PORT, port=REDIS_PORT)
