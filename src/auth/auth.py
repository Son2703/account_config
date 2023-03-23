
from datetime import datetime, timedelta
from functools import wraps
import secrets
from bson import ObjectId

from flask import jsonify, request
import jwt

from configs.base import SECRET_KEY
from configs.configs import Authen
from src.models.mongo.list_pass_user_db import MGListPassUser
from src.models.mongo.merchant_cf_db import MGconfig
from src.models.mongo.rule_db import MGRule
from src.models.mongo.user_db import MGUser


def create_access_token(data: dict, expires_delta: timedelta = None):
        user_info = data.copy()

        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=59)


        user_info.update({"exp": expire})
        
        token = jwt.encode(user_info, SECRET_KEY, algorithm=Authen.ALGORITHM)
        return token

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # jwt is passed in the request header
        if 'Authorization' in request.headers:
            token = request.headers['Authorization']
        # return 401 if token is not passed
        if not token:
            return jsonify({'message' : 'Token is missing !!'}), 401
  
            # decoding the payload to fetch the stored details
        data = jwt.decode(token, SECRET_KEY, algorithms=Authen.ALGORITHM)
        current_user = MGUser().filter_one({"_id": ObjectId(data["id_user"]), "id_merchant": data["id_merchant"]})
        if not bool(current_user):
            return jsonify({"message": "Invalid token!"}), 401
        # returns the current logged in users context to the routes
        return  f(*args, **kwargs)

    return decorated



def get_data_by_decode():
    token = request.headers['Authorization']
    data = jwt.decode(token, SECRET_KEY, algorithms=Authen.ALGORITHM)
    return data["id_merchant"], data["id_user"]