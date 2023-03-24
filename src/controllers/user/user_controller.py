import json
from src.apis import *
from bson import json_util
from flask import Blueprint
from src.apis import response
from bson.objectid import ObjectId
from flask import jsonify, request
from bson.json_util import loads, dumps
from src.common.common import CommonKey
from src.common.constants import Status
from src.models.mongo.user_db import MGUser
from werkzeug.security import generate_password_hash, check_password_hash
from src.controllers.user.validator import ValidateUser as validate
from src.auth.auth import get_data_by_decode
from src.auth.rules import RuleAuth

# from producer import MessageProducer
# from consumer import MessageConsumer
import pandas as pd
from kafka import KafkaProducer

broker = 'localhost:9092'
topic = 'test-topic'
group_id = 'consumer-1'

app = Blueprint('app', __name__)


class UserControllers():
    def __init__(self):
        pass

    def create(self):
        try:
            merchant_id, user_id = get_data_by_decode()
            body_data = request.get_json()
            error_val_name = RuleAuth.validate_name(body_data[CommonKey.USERNAME], merchant_id)
            if bool(error_val_name):
                return error_val_name
            error_val_pass = RuleAuth.validate_pass(body_data[CommonKey.PASSWORD], merchant_id)
            if bool(error_val_pass):
                return error_val_pass
            if bool(validate.validate_add_user(body_data)):
                return validate.validate_add_user(body_data)

            if MGUser().filter_one({CommonKey.USERNAME: body_data[CommonKey.USERNAME], CommonKey.ID_MERCHANT: merchant_id}):

                return response.bad_request("{} is already taken".format(CommonKey.USERNAME))

            data_final = {
                CommonKey.USERNAME: body_data[CommonKey.USERNAME],
                CommonKey.PASSWORD: generate_password_hash(body_data[CommonKey.PASSWORD]),
                CommonKey.ID_MERCHANT: merchant_id,
                CommonKey.STATUS: Status.ACTIVATE.value,
                CommonKey.LAST_LOGIN: None,
                CommonKey.LOGIN_FAIL_NUMBER: 0
            }
            if MGUser().create(data_final, user_id):
                return build_response_message()
            else:
                return bad_request()

        except Exception as e:
            print(e, flush=True)

    def change_pass(self):
        try:
            merchant_id, user_id = get_data_by_decode()
            body_data = request.get_json()
            if bool(validate.validate_change_pass(body_data)):
                return validate.validate_change_pass(body_data)

            user = MGUser().filter_one({CommonKey.USERNAME: body_data[CommonKey.USERNAME], CommonKey.ID_MERCHANT: merchant_id})
            if not user:
                return response.not_found()

            if not check_password_hash(user[CommonKey.PASSWORD], body_data[CommonKey.PASSWORD]) or user[CommonKey.USERNAME] != body_data[CommonKey.USERNAME]:
                return response.bad_request("{} hoặc {} không chính xác".format(CommonKey.USERNAME, CommonKey.PASSWORD))

            if body_data[CommonKey.NEW_PASSWORD] != body_data[CommonKey.PASSWORD_CONFIRM]:
                return response.bad_request("Xác nhận {} không chính xác".format(CommonKey.PASSWORD))

            data_final = {CommonKey.PASSWORD: generate_password_hash(
                body_data[CommonKey.NEW_PASSWORD])}

            if MGUser().update_one(query={CommonKey.ID: ObjectId(user_id)},
                                   payload=data_final,
                                   updater=user_id):

                return build_response_message()
            else:
                return bad_request()

        except Exception as e:
            print(e, flush=True)

    def get_user(self, id_user):
        try:
            merchant_id, _ = get_data_by_decode()
            user = MGUser().filter_one(payload={CommonKey.ID: ObjectId(id_user), CommonKey.ID_MERCHANT: merchant_id},
                                       projection={CommonKey.ID: 0, CommonKey.PASSWORD: 0})
            if user:
                return build_response_message(json.loads(json_util.dumps(user)))
            else:
                return bad_request()
        except Exception as e:
            print(e, flush=True)

    def lock_user(self):
        try:
            merchant_id, user_id = get_data_by_decode()

            body_data = request.get_json()
            if validate.validate_lock_user(body_data) != False:
                return validate.validate_lock_user(body_data)

            if MGUser().filter_one({CommonKey.ID: body_data[CommonKey.ID_USER]}):
                return response.not_found()

            data_final = {CommonKey.STATUS: Status.DEACTIVE.value}

            if MGUser().update_one(query={CommonKey.ID: ObjectId(body_data[CommonKey.ID_USER]), CommonKey.ID_MERCHANT: merchant_id},
                                   payload = data_final,
                                   updater = user_id):

                return build_response_message()
            else:
                return bad_request()

        except Exception as e:
            print(e, flush=True)

    def delete_user(self, user_id):
        try:
            merchant_id, _ = get_data_by_decode()
            if MGUser().filter_one({CommonKey.ID: ObjectId(user_id), CommonKey.ID_MERCHANT: merchant_id}):
                if MGUser().detele_one({CommonKey.ID: ObjectId(user_id), CommonKey.ID_MERCHANT: merchant_id}):
                    return build_response_message()
                else:
                    return bad_request()
            else:
                return not_found
        except Exception as e:
            print(e, flush=True)

    def bulk_insert(self):
        try:
            body_data = request.get_json()

            return jsonify({"code": 200, "message": body_data}), 200
        except Exception as e:
            print(e)


    def excel_insert(self):
        fileExcel = request.files['file']
        
        if fileExcel.filename.endswith('.csv'):
            df = pd.read_csv(fileExcel)         
        elif fileExcel.filename.endswith('.xlsx'):
            df = pd.read_excel(fileExcel, engine='openpyxl')
        else:
            return response.bad_request("File không đúng định dạng")
        
        data = df.to_dict(orient='records')


        return response.success(data)
