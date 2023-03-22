from flask import jsonify, request
from src.models.mongo.user_model import UserModel
from bson.objectid import ObjectId
from flask import Blueprint
from werkzeug.security import generate_password_hash
from src.common.validator import ValidateUser
# from producer import MessageProducer
# from consumer import MessageConsumer

broker = 'localhost:9092'
topic = 'test-topic'
group_id = 'consumer-1'

app = Blueprint('app', __name__)


class UserControllers():
    def __init__(self):
        pass

    def Register(self):
        try:

            body_data = request.get_json()
            if ValidateUser.validate_add_user(body_data) != False:
                return ValidateUser.validate_add_user(body_data)
            
            data_final = {
                "username": body_data["username"],
                "password": generate_password_hash(body_data["password"]),
                "id_merchant": 1,
                "status" :1,
                "login_fail_number": 0
            }
            # Fake cretor
            cretor = ObjectId()
            if UserModel().create(data_final, cretor):
                return jsonify({"code": 200, "message": "User has been registered"}), 200
            else:
                return jsonify({"code": 400, "message": "Fail to register user"}), 400
            
        except Exception as e:
            print(e)
   
    def ChangePass(self, user_id):
        try:
            body_data = request.get_json()
            if ValidateUser.validate_change_pass(body_data, user_id) != False:
                return ValidateUser.validate_change_pass(body_data, user_id)

            data_final = {"password": generate_password_hash(body_data["new_password"])}

            if UserModel().update_one(query = {"_id": ObjectId(user_id)}, 
                                      payload = data_final, 
                                      updater = ObjectId(user_id)):
                
                return jsonify({"code": 200, "message": "Change password successfully"}), 200
            else:
                return jsonify({"code": 400, "message": "Fail to change password"}), 400
         
        except Exception as e:
            print(e)

    def GetUser(self, user_id):
        try:
            user = UserModel().filter_one({"_id": ObjectId(user_id)})
            if user:                
                return jsonify({
                    'code': 200,
                    'message': 'Success 12312',
                    'results': {
                        "username" : user["username"],
                        "password" : user["password"],
                        "id_merchant":user["id_merchant"],
                        "status": user["status"]
                    }
                })
                return jsonify({"code": 200, "message": "Change password successfully"}), 200
        except Exception as e:
            print(e)

    def LockUser(self):
        try:
            body_data = request.get_json()
            if ValidateUser.validate_lock_user(body_data) != False:
                return ValidateUser.validate_lock_user(body_data)
            data_final = {"status": 2}

            if UserModel().update_one(query = {"_id": ObjectId(body_data["user_id"])}, 
                                      payload = data_final, 
                                      updater="1231244"):
                
                return jsonify({"code": 200, "message": "Lock User Successfully"}), 200
            else:
                return jsonify({"code": 400, "message": "Fail to Lock User"}), 400

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
