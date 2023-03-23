

from datetime import timedelta
from bson import ObjectId, json_util
import json
from flask import Blueprint, request
from src.auth.auth import create_access_token
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

        match_password = check_password_hash(
            current_user[CommonKey.PASSWORD], data[CommonKey.PASSWORD])
        if not match_password:
            return unauthor(Message.NOT_MATCH_PASSWORD)


        data_jwt = json.loads(json_util.dumps({CommonKey.ID_USER: str(
            current_user[CommonKey.ID]), CommonKey.ID_MERCHANT: current_user[CommonKey.ID_MERCHANT]}))

        token = create_access_token(
            data=data_jwt, expires_delta=timedelta(days=TimeChoise.ONE_HOUR.value))
    except Exception as e:
        print(e, flush=True)
    return build_response_message({"Authorization": token})
