from configs.base import *
import pymongo

# mongodb://config-account-mongo
# mongodb://localhost:27017/
Mongo_Client = pymongo.MongoClient(
    host="config-account-mongo", port=27017, username=MONGO_USERNAME, password=MONGO_PASSWORD)

Mongo_Client = pymongo.MongoClient(
    host="config-account-mongo", port=27017, username= MONGO_USERNAME, password=MONGO_PASSWORD)

CONFIG_ACCOUNT_DB = Mongo_Client[MONGO_DB]
RULE_COL_NAME = CONFIG_ACCOUNT_DB[RULE_COL_NAME]
CONFIG_ACCOUNT_DB = Mongo_Client[MONGO_DB]
USER_COL_NAME = CONFIG_ACCOUNT_DB[USER_COL_NAME]

import redis

Redis_Client = redis.StrictRedis(host=REDIS_PORT, port=REDIS_PORT)

class Authen:
    ALGORITHM = "HS256"