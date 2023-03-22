from flask import jsonify, request, render_template
from src.models.mongo.user_model import UserModel
from bson.objectid import ObjectId
from mobio.libs.validator import HttpValidator, VALIDATION_RESULT, Length, \
Required, InstanceOf, Pattern
from werkzeug.security import check_password_hash
from src.apis import response


class ValidateUser():
    def validate_add_user(input_data):
        try: 
            validate_pass = [Required, InstanceOf(str)]
            # validate_pass.append(Pattern(r"(^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])[0-9a-zA-Z]{8,}$)"))
            users_validate = {
                'username': [Required, InstanceOf(str)],
                # 'password': [Required, InstanceOf(str), Length(4, 9), Pattern(r"(^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])[0-9a-zA-Z]{8,}$)")],
                # ^[0-9]{5}[!@#$%^&*()_+|~-]{7}$
                'password': validate_pass
            }
            valid = HttpValidator(users_validate)
            val_result = valid.validate_object(input_data)
            
            if not val_result[VALIDATION_RESULT.VALID]:
                return jsonify({"code": 409, "message": val_result[VALIDATION_RESULT.ERRORS]})
            
            if UserModel().filter_one({"username": input_data["username"]}):
                    return jsonify({"code": 409, "message": "Username is already taken"})
            
            return False
        except Exception as e:
                print(e)
    def validate_change_pass(input_data, user_id):
        try:
            users_validate =  {
                    'username': [Required, InstanceOf(str)],
                    'password': [Required, InstanceOf(str)],
                    'new_password': [Required, InstanceOf(str)],
                    'password_confirm': [Required, InstanceOf(str)]
                }
            valid = HttpValidator(users_validate)
            val_result = valid.validate_object(input_data)
            
            if not val_result[VALIDATION_RESULT.VALID]:
                return jsonify({"code": 409, "message": val_result[VALIDATION_RESULT.ERRORS]})

            user = UserModel().filter_one({"_id": ObjectId(user_id)})

            if  check_password_hash(user["username"], input_data["username"]):
                return jsonify({"code": 409, "message": "username not match"})

            if not check_password_hash(user["password"], input_data["password"]):
                return jsonify({"code": 409, "message": "password not match"})

            if input_data["new_password"] != input_data["password_confirm"]:
                return jsonify({"code": 409, "message": "New password not match"})
            
            # if check_password_hash(user["password"], input_data["password_confirm"]):
            #      return jsonify({"code": 200, "message": "Change password successfully 123"}), 200
            return False
        except Exception as e:
                print(e)
    
    def validate_lock_user(input_data):
        try:
            users_validate =  {
                'user_id': [Required, InstanceOf(str)]
                    
            }
            valid = HttpValidator(users_validate)
            val_result = valid.validate_object(input_data)
            
            if not val_result[VALIDATION_RESULT.VALID]:
                return jsonify({"code": 409, "message": val_result[VALIDATION_RESULT.ERRORS]})
            user = UserModel().filter_one({"_id": ObjectId(input_data["user_id"])})
            if not user:
                return jsonify({"code": 409, "message": "user not exist"})
            return False
        except Exception as e:
            print(e)