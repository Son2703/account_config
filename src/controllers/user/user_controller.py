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

# from producer import MessageProducer
# from consumer import MessageConsumer

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
            if bool(validate.validate_add_user(body_data)):
                return validate.validate_add_user(body_data)

            if MGUser().filter_one({CommonKey.USERNAME: body_data[CommonKey.USERNAME], CommonKey.ID_MERCHANT: merchant_id}):
                # return bad_request(BaseMoError("already_exist", "EEE", "OOO"))

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

            user = MGUser().filter_one({CommonKey.ID: ObjectId(
                user_id), CommonKey.ID_MERCHANT: merchant_id})
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

            print(body_data["id_user"], flush= True)
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
            # if ValidateUser.validate_change_pass(body_data) != False:
            #     return ValidateUser.validate_change_pass(body_data)

            return jsonify({"code": 200, "message": body_data}), 200
        except Exception as e:
            print(e)


# class UserController:
#     def __init__(self):
#         self.user_manager = MGUser()

#     @app.route("/users", methods=["POST"])
#     def register(self):
#         data = {
#             'username': request.json["username"],
#             'password': request.json["password"]
#         }
#         # Kiểm tra xem tên người dùng đã tồn tại hay chưa
#         if self.user_manager.get_by_username(data["username"]):
#             return jsonify({"success": False, "message": "Username is already taken"})

#         # Tạo user mới và lưu vào database
#         rs = self.user_manager.create(payload=data)
#         if rs:
#             return jsonify({"success": True, "message": "User has been registered"}), 200
#         else:
#             return jsonify({"success": False, "message": "Fail to register user"}), 400

    # @app.route("/users", methods=["POST"])
    # def register(self):

    #     users = {
    #         'username': [Required, InstanceOf(str)],
    #         # 'password': [Required, InstanceOf(str), Length(4, 9), Pattern(r"(^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])[0-9a-zA-Z]{8,}$)")],
    #         'password': [Required, InstanceOf(str), Length(4, 9)]
    #     }

    #     data = {
    #         'username': request.json["username"],
    #         'password': request.json["password"]
    #     }

    #     valid = HttpValidator(users)
    #     val_result = valid.validate_object(data)
    #     if not val_result[VALIDATION_RESULT.VALID]:
    #         return jsonify({"code": 400, "message": val_result[VALIDATION_RESULT.ERRORS]}), 400

    #     if self.user_manager.get_by_username(data["username"]):
    #         return jsonify({"success": False, "message": "Username is already taken"})

    #     return jsonify({"code": 200, "message": "User has been registered"}), 200

        # else:

        #     rs = MGUser().create(payload=data)
        #     if rs:
        #         return jsonify({"code": 200, "message": "User has been registered"}), 200
        #     else:
        #         return jsonify({"code": 400, "message": "fail"}), 200

    #     send_message = {"username": data['username'], 'email': data['email'], 'password': data['password'], 'type': request.method, 'route' : 'register', "function": 'create'}
    #     message_producer = MessageProducer(broker, topic)
    #     if message_producer.send_msg(send_message):
    #         return jsonify({"success": True, "message": "User has been registered"}), 200
