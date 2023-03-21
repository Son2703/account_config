import os
from dotenv import load_dotenv

load_dotenv()

#host mobio
HOST=os.getenv("HOST")
ADMIN_HOST=os.getenv("ADMIN_HOST")

#redis
REDIS_NAME = os.getenv("REDIS_NAME")
REDIS_PORT = os.getenv("REDIS_PORT")
REDIS_PORT = os.getenv("REDIS_PORT")

#mongo
MONGO_USERNAME=os.getenv("MONGO_USERNAME")
MONGO_PASSWORD=os.getenv("MONGO_PASSWORD")
MONGO_DB = os.getenv("MONGO_DB")
SECRET_KEY = os.getenv("SECRET_KEY")