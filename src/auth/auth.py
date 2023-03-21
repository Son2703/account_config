
from datetime import datetime, timedelta
from functools import wraps
import secrets
from bson import ObjectId

from flask import jsonify, request
import jwt
import pymongo

from configs.base import SECRET_KEY
from configs.configs import Authen
from src.common.constants import Rule
from src.common.time import timestamp_utc
from src.models.mongo.list_pass_user_db import MGListPassUser
from src.models.mongo.merchant_rule_assignment import MGMerchantRuleAssignment
from src.models.mongo.rule_db import MGRule
from src.models.mongo.user_db import MGUser


rule_table = MGRule()
user_table = MGUser()
merchant_rule_assignment_table = MGMerchantRuleAssignment()
list_pass_user_table = MGListPassUser()


def create_access_token(data: dict, expires_delta: timedelta = None):
    user_info = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=59)

    user_info.update({"exp": expire})

    token = jwt.encode(user_info, SECRET_KEY, algorithm=Authen.ALGORITHM)
    update_last_login(user_info)
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
            return jsonify({'message': 'Token is missing !!'}), 401

        try:
            # decoding the payload to fetch the stored details
            data = jwt.decode(token, SECRET_KEY, algorithms=Authen.ALGORITHM)
            current_user = user_table.filter_one({"_id": data["_id"]})
        except:
            return jsonify({
                'message': 'Token is invalid !!'
            }), 401
        # returns the current logged in users context to the routes
        update_last_login(current_user)

        return f(current_user, *args, **kwargs)
    return decorated


def need_change_password_first(user_info: dict):
    rule = rule_table.filter_one({"name": Rule.REQUIRE_CHANGE_PASS.value})
    # check rule is active
    if not rule:
        return

    if not rule["status"]:
        return

    # check config is active
    config = merchant_rule_assignment_table.filter_one(
        {"id_rule": ObjectId(rule["_id"]), "id_merchant": ObjectId(user_info["id_merchant"])})
    if not config:
        return

    if not config["status"]:
        return

    password_list_length = list_pass_user_table.find(
        {"id_user": ObjectId(user_info["_id"])})
    if len(password_list_length) != 1:
        return

    return True


def lock_account(user_info: dict):
    rule = rule_table.filter_one({"name": Rule.LOCK_ACCOUNT.value})
    # check rule is active
    if not rule:
        return

    if not rule["status"]:
        return

    # check config is active
    config = merchant_rule_assignment_table.filter_one(
        {"id_rule": ObjectId(rule["_id"]), "id_merchant": ObjectId(user_info["id_merchant"])})
    if not config:
        return

    if not config["status"]:
        return

    result = user_table.update_without_updater(
        query={"_id": ObjectId(user_info["_id"])},
        payload={
            "login_fail_number": user_info["login_fail_number"]+1,
            "last_login": timestamp_utc()
        }
    )


def get_verify_user_configs(user_info: dict):
    if need_change_password_first(user_info):
        return {"code": Rule.REQUIRE_CHANGE_PASS.value, "message": "You need to change password at the first time login!"}
    if need_change_pass_after(user_info):
        return {"code": Rule.REQUIRE_CHANGE_PASS.value, "message": "You need to change password!"}
    return


def update_last_login(user_info: dict):

    try:
        result = user_table.update_without_updater(
            query={"_id": ObjectId(user_info["_id"])},
            payload={"last_login": timestamp_utc()}
        )
        return result
    except Exception as error:
        raise error


def check_lock_time(user_info: dict):

    rule = rule_table.filter_one({"name": Rule.LOCK_ACCOUNT.value})
    # check rule is active
    if not rule:
        return

    if not rule["status"]:
        return

    # check config is active
    config = merchant_rule_assignment_table.filter_one(
        {"id_rule": rule["_id"], "id_merchant": user_info["id_merchant"]})

    if not config:
        return

    if not config["status"]:
        return
    if user_info["login_fail_number"] != config["value"]:
        return
    last_login = datetime.fromtimestamp(
        user_info["last_login"] or timestamp_utc())
    expire_time = last_login + timedelta(minutes=int(config["time_lock"]))

    if expire_time < datetime.utcnow():  # reset expire time
        result = user_table.update_one(
            query={"_id": ObjectId(user_info["_id"])},
            payload={
                "login_fail_number": 0,
                "last_login": timestamp_utc()
            }
        )
        return

    return {"code": Rule.LOCK_ACCOUNT.value, "message": f'Account will unlock after {int(config["time_lock"])} minutes'}


def need_change_pass_after(user_info):
    rule = rule_table.filter_one({"name": Rule.CHANGE_PASS_MOTH.value})
    # check rule is active
    if not rule:
        return

    if not rule["status"]:
        return

    # check config is active
    config = merchant_rule_assignment_table.filter_one(
        {"id_rule": rule["_id"], "id_merchant": user_info["id_merchant"]})

    if not config:
        return

    if not config["status"]:
        return
    
    last_time_change_password = list_pass_user_table.filter_one({"id_user": ObjectId(user_info["_id"])}).sort([("created_at", pymongo.DESCENDING)])

    print("LASTTT", last_time_change_password, flush=True)