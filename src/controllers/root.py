

from datetime import timedelta
from bson import ObjectId, json_util
import json
from flask import Blueprint, request
from marshmallow import ValidationError
from src.auth.auth import create_access_token
from src.helps.func import get_json_from_db
from src.models.mongo.user_db import MGUser

from src.common.common import CommonKey
from src.models.schemas.user_schemas import SignInSchema
from werkzeug.security import check_password_hash


root_url = Blueprint('root', __name__)


@root_url.route("/login", methods=["POST"])
def login():
    try:
        # data = SignInSchema().load(request.json)

        # current_user = MGUser().filter_one({
        #     CommonKey.USERNAME: data[CommonKey.USERNAME],
        #     CommonKey.ID_MERCHANT: ObjectId(data[CommonKey.ID_MERCHANT]),
        #     CommonKey.STATUS: 1
        # })
        # if current_user is None:
        #     return {"code": 404, "message": "User not found!"}, 404

        # match_password = check_password_hash(
        #     current_user[CommonKey.PASSWORD], data[CommonKey.PASSWORD])
        # if not match_password:
        #     return {"code": 403, "message": "Login fail!"}, 403
        current_user = {
            CommonKey.ID_MERCHANT: "merchant_1",
            CommonKey.ID: ObjectId(),
        }

        data_jwt = json.loads(json_util.dumps({CommonKey.ID_USER: str(
            current_user[CommonKey.ID]), CommonKey.ID_MERCHANT: current_user[CommonKey.ID_MERCHANT]}))

        token = create_access_token(
            data=data_jwt, expires_delta=timedelta(days=1))

    except ValidationError as err:
        return {CommonKey.CODE: 400, "message": err.messages}, 400
    return {"code": 200, "data": {"token": token}}
