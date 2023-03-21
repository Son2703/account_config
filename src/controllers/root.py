

from datetime import timedelta
<<<<<<< HEAD
import datetime
from bson import ObjectId
=======
from bson import ObjectId, json_util
import json
>>>>>>> 0118348 (fix login)
from flask import Blueprint, request
from marshmallow import ValidationError
from src.auth.auth import check_lock_time, create_access_token, get_verify_user_configs, lock_account, need_change_password_first, update_last_login
from src.common.time import timestamp_utc
from src.helps.func import get_json_from_db
from src.models.mongo.user_db import MGUser

from src.common.common import CommonKey
from src.models.schemas.user_schemas import SignInSchema
from werkzeug.security import check_password_hash


root_url = Blueprint('root', __name__)


@root_url.route("/login", methods=["POST"])
def login():
    try:
        data = SignInSchema().load(request.json)

        current_user = MGUser().filter_one({
            CommonKey.USERNAME: data[CommonKey.USERNAME],
            CommonKey.ID_MERCHANT: ObjectId(data[CommonKey.ID_MERCHANT]),
            CommonKey.STATUS: 1
        })
        if current_user is None:
            return {"code": 404, "message": "User not found!"}, 404

        match_password = check_password_hash(
            current_user[CommonKey.PASSWORD], data[CommonKey.PASSWORD])
        if not match_password:
            return {"code": 403, "message": "Login fail!"}, 403

        data_jwt = json.loads(json_util.dumps({CommonKey.ID_USER: str(
            current_user[CommonKey.ID]), CommonKey.ID_MERCHANT: current_user[CommonKey.ID_MERCHANT]}))

        token = create_access_token(
            data=data_jwt, expires_delta=timedelta(days=1))

    except ValidationError as err:
        return {CommonKey.CODE: 400, "message": err.messages}, 400
    return {"code": 200, "data": {"token": token}}
