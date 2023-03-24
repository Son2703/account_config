from src.apis import * 
from src.apis import response
from bson.objectid import ObjectId
from src.common.common import CommonKey
from src.models.mongo.user_db import MGUser
from flask import jsonify, request, render_template
from mobio.libs.validator import HttpValidator, VALIDATION_RESULT, Length, \
    Required, InstanceOf


class ValidateUser():
    def validate_add_user(input_data):
        try:
            user_validate = {
                CommonKey.USERNAME: [Required, InstanceOf(str)],
                CommonKey.PASSWORD: [Required, InstanceOf(str)]
            }
            valid = HttpValidator(user_validate)
            val_result = valid.validate_object(input_data)

            if not val_result[VALIDATION_RESULT.VALID]:
                return response.bad_request(val_result[VALIDATION_RESULT.ERRORS])

            return False
        except Exception as e:
            print(e)

    def validate_change_pass(input_data):
        try:
            user_validate = {
                CommonKey.USERNAME: [Required, InstanceOf(str)],
                CommonKey.PASSWORD: [Required, InstanceOf(str)],
                CommonKey.NEW_PASSWORD: [Required, InstanceOf(str)],
                CommonKey.PASSWORD_CONFIRM: [Required, InstanceOf(str)]
            }
            valid = HttpValidator(user_validate)
            val_result = valid.validate_object(input_data)

            if not val_result[VALIDATION_RESULT.VALID]:
                return response.bad_request(val_result[VALIDATION_RESULT.ERRORS])

            return False
        except Exception as e:
            print(e)

    def validate_lock_user(input_data):
        try:
            user_validate = {
                CommonKey.ID_USER: [Required, InstanceOf(str)]
            }
            valid = HttpValidator(user_validate)
            val_result = valid.validate_object(input_data)

            if not val_result[VALIDATION_RESULT.VALID]:
                return response.bad_request(val_result[VALIDATION_RESULT.ERRORS])

            return False
        except Exception as e:
            print(e)

    def validate_bulk_insert(input_data):
        try:
            user_validate = {
                CommonKey.USERNAME: [Required, InstanceOf(str)],
                CommonKey.PASSWORD: [Required, InstanceOf(str)]
            }
            valid = HttpValidator(user_validate)
            val_result = valid.validate_object(input_data)
            if not val_result[VALIDATION_RESULT.VALID]:
                return response.bad_request(val_result[VALIDATION_RESULT.ERRORS])
            return False

        except Exception as e:
            print(e)
