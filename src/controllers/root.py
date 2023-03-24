

from datetime import timedelta
from bson import ObjectId, json_util
import json
from flask import Blueprint, request
from src.auth.auth import create_access_token
from marshmallow import ValidationError
from src.apis import HTTP
from src.auth.auth import check_lock_time, create_access_token, get_verify_user_configs, lock_account, need_change_password_first, update_last_login
from src.common.common import CommonKey
from src.helps.func import get_json_from_mongo
from src.models.mongo.user_db import MGUser
from src.apis import *
from src.common.constants import *
from src.common.common import CommonKey
from src.common.message import Message
from src.models.schemas.user_schemas import SignInSchema
from werkzeug.security import check_password_hash


root_url = Blueprint('root', __name__)


@root_url.route("/login", methods=[HTTP.METHOD.POST])
def login():
    try:
        data = SignInSchema().load(request.json)

        current_user = MGUser().filter_one({
            CommonKey.USERNAME: data[CommonKey.USERNAME],
            CommonKey.ID_MERCHANT: ObjectId(data[CommonKey.ID_MERCHANT]),
        })

        if current_user[CommonKey.STATUS] != Status.ACTIVATE.value:
            return unauthor(Message.USER_NOT_ACTIVATE)

        if not bool(current_user):
            return not_found(Message.NOT_EXIST, CommonKey.USERNAME, data[CommonKey.USERNAME])

        # check account lock
        result_lock_time = check_lock_time(current_user)
        if result_lock_time:
            return {"code": 401, "error": result_lock_time}, 401

        match_password = check_password_hash(
            current_user[CommonKey.PASSWORD], data[CommonKey.PASSWORD])

        user_json = get_json_from_mongo(current_user)

        if not match_password:
            lock_account(current_user)
            return {"code": 403, "message": "Login fail!"}, 403
        # current_user = {
        #     CommonKey.ID_MERCHANT: "merchant_1",
        #     CommonKey.ID: ObjectId(),
        # }

        config_mess = get_verify_user_configs(user_json)
        if config_mess:
            update_last_login(user_json)
            return {"code": 401, "error": config_mess}, 401

        data_jwt = json.loads(json_util.dumps({CommonKey.ID_USER: str(
            current_user[CommonKey.ID]), CommonKey.ID_MERCHANT: current_user[CommonKey.ID_MERCHANT]}))

        token = create_access_token(
            data=data_jwt, expires_delta=timedelta(days=1))

    except ValidationError as err:
        return {CommonKey.CODE: 400, "message": err.messages}, 400

    update_last_login(current_user)

    return {"code": 200, "data": {"token": token}}
