

from datetime import timedelta
import datetime
from bson import ObjectId
from flask import Blueprint, request
from marshmallow import ValidationError
from src.auth.auth import check_lock_time, create_access_token, get_verify_user_configs, lock_account, need_change_password_first, update_last_login
from src.common.time import timestamp_utc
from src.helps.func import get_json_from_db
from src.models.mongo.user_db import MGUser

from src.models.schemas.user_schemas import SignInSchema
from werkzeug.security import check_password_hash


root_url = Blueprint('root', __name__)

@root_url.route("/login", methods=["POST"])
def login():
    body = request.get_json()

    try:
        val_body = SignInSchema().load(body)
    except ValidationError as err:
        return {"code": 400, "message": err.messages}, 400
    
    val_body["id_merchant"] = ObjectId(val_body["id_merchant"])
    current_user = MGUser().filter_one({
        "username": val_body["username"],
        "id_merchant": val_body["id_merchant"],
        "status": 1
    })

    if current_user is None:
        return {"code": 404, "message": "User not found!"}, 404
    
    # check account lock
    result_lock_time = check_lock_time(current_user)
    if result_lock_time:
        return {"code": 401, "error": result_lock_time}, 401

    match_password = check_password_hash(current_user["password"], val_body["password"])

    user_json = get_json_from_db(current_user)

    if not match_password:
        lock_account(current_user)
        return {"code": 403, "message": "Login fail!"}, 403
    
    
    config_mess = get_verify_user_configs(user_json)
    if config_mess:
        update_last_login(user_json)
        return {"code": 401, "error": config_mess}, 401

    token = create_access_token(data=user_json, expires_delta=timedelta(days=1)) 

    return {"code": 200, "data": {"token": token}}