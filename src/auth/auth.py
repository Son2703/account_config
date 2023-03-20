
from datetime import timedelta
import datetime
from functools import wraps
import secrets

from flask import jsonify, request
import jwt

from configs.base import SECRET_KEY
from configs.configs import Authen
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
  
        try:
            # decoding the payload to fetch the stored details
            data = jwt.decode(token, SECRET_KEY, algorithms=Authen.ALGORITHM)
            current_user = MGUser().query\
                .filter_by(public_id = data['public_id'])\
                .first()
        except:
            return jsonify({
                'message' : 'Token is invalid !!'
            }), 401
        # returns the current logged in users context to the routes
        return  f(current_user, *args, **kwargs)
  
    return decorated