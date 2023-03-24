from configs.base import *
import pymongo
from bson import ObjectId

Mongo_Client = pymongo.MongoClient(
    host="config-account-mongo", port=27017, username=MONGO_USERNAME, password=MONGO_PASSWORD)

Mongo_Client = pymongo.MongoClient(
    host="config-account-mongo", port=27017, username= MONGO_USERNAME, password=MONGO_PASSWORD)

CONFIG_ACCOUNT_DB = Mongo_Client[MONGO_DB]

import redis

Redis_Client = redis.StrictRedis(host=REDIS_PORT, port=REDIS_PORT)

class Authen:
    ALGORITHM = "HS256"



mycol_merchant = CONFIG_ACCOUNT_DB["merchants"]
mycol_user = CONFIG_ACCOUNT_DB["users"]

# mycol_merchant.delete_many({})
# mycol_user.delete_many({})

# data = {"name": "mobio",
#   "create_by": None,
#   "update_by": None,
#   "create_at": 1679299998.002571,
#   "update_at": None,
#   "status": 1}

# data_1 = {"username": "mobiadmin", 
#     "role": "admin",
#     "password": "pbkdf2:sha256:260000$6OdBOS0LLMwmTSi0$d982228897b2d50eb2f3273ee4511acdf16f331966b6af5865aa9b7388388db7", 
#     "id_merchant": 0,
#     "status": 1,
#     "last_login": None,
#     "login_fail_number": 0,
#     "create_by": None,
#     "update_by": None,
#     "create_at": None,
#     "update_at": None}

# id_mer = None
# if mycol_merchant.find_one({"name": "mobio"}) == None:
#     c = mycol_merchant.insert_one(data)
#     id_mer = c.inserted_id
# else :
#     a = mycol_merchant.find_one({"name": "mobio"}) 
#     id_mer = str(a["_id"])


# data_1 = {"username": "mobiadmin", 
#     "role": "admin",
#     "password": "pbkdf2:sha256:260000$6OdBOS0LLMwmTSi0$d982228897b2d50eb2f3273ee4511acdf16f331966b6af5865aa9b7388388db7", 
#     "id_merchant": id_mer,
#     "status": 1,
#     "last_login": None,
#     "login_fail_number": 0,
#     "create_by": None,
#     "update_by": None,
#     "create_at": None,
#     "update_at": None}

# if mycol_user.find_one({"username": "mobiadmin", "id_merchant": id_mer}) == None:
#     c = mycol_user.insert_one(data_1)


print([i for i in mycol_merchant.find()], flush=True)
print([i for i in mycol_user.find()], flush=True)

# 641d5464f12b7755a1c13d5d


# # 641d53f6fdb5d8085a60c763
# # 641d53f6fdb5d8085a60c764

# # 641d5427c28848ebd29595cd
# # 641d5427c28848ebd29595ce

# # CONFIG_ACCOUNT_DB["users"].create({"username": "mobiadmin", 
# #   "role": "admin",
# #   "password": "pbkdf2:sha256:260000$6OdBOS0LLMwmTSi0$d982228897b2d50eb2f3273ee4511acdf16f331966b6af5865aa9b7388388db7", 
# #   "id_merchant": O,
# #   "status": 1,
# #   "last_login": None,
# #   "login_fail_number": 0,
# #   "create_by": None,
# #   "update_by": None,
# #   "create_at": None,
# #   "update_at": None})