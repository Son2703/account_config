from flask import request,jsonify
from src.models.mongo.rule_db import MGRule
from bson import ObjectId,json_util
from mobio.libs.logging import MobioLogging
from mobio.sdks.base.controllers import BaseController
from mobio.libs.validator import Required, InstanceOf, In
from src.common.constants import LIST_RULE_NAME
from mobio.libs.validator import Validator, HttpValidator, VALIDATION_RESULT, Length, Required, InstanceOf, In, Password, Pattern
from src.apis import response
from src.common.common import is_ObjectID_valid
from src.common.common import CommonKey
import math, jwt, json
from configs.base import SECRET_KEY
from configs.configs import Authen
from src.auth.auth import get_data_by_decode

class RuleControllers(BaseController):
    def __init__(self):
        BaseController().__init__()

    def validate_add_rule(self, input_data):
        rule_validate = {
            CommonKey.NAME: [Required, In(LIST_RULE_NAME)],
            CommonKey.STATUS: [InstanceOf(bool)]
        }

        valid = HttpValidator(rule_validate)
        val_result = valid.validate_object(input_data)
        
        if not val_result[VALIDATION_RESULT.VALID]:
            return response.bad_request(val_result[VALIDATION_RESULT.ERRORS])
        
        #Name already exists
        querry_name = {CommonKey.NAME: input_data[CommonKey.NAME]}
        if MGRule().count_documents(querry_name) > 0:
            return response.bad_request("Rule đã có trong hệ thống")
        
        return False
    
    def validate_get_list_rule(self, params):
        
        if CommonKey.PAGE not in params:
            page = 1
        else:
            page = params[CommonKey.PAGE]

        if CommonKey.PERPAGE not in params:
            perpage = 6
        else:
            perpage = params[CommonKey.PERPAGE]

        try: 
            page = int(page)
            perpage = int(perpage)
        except:
            return response.bad_request("Page, perpage phải là số  nguyên"), None, None
    
        return False, page, perpage
    
    def validate_get_one_rule(self, rule_id):

        if is_ObjectID_valid(rule_id) == False:
            return response.bad_request("ID không hợp lệ")
        
        querry = {"_id": ObjectId(rule_id)}
        if MGRule().count_documents(querry) == 0:
            return response.bad_request("Rule không có trong hệ thống")

        return False
    
    def validate_list_rule(self, list_rule):
        list_rule_satisfy = []
        list_rule_not_satisfy = []

        for rule_id in list_rule:
            if (self.validate_get_one_rule(rule_id) == False):
                list_rule_satisfy.append(rule_id)
            else:
                list_rule_not_satisfy.append(rule_id)
        
        return list_rule_satisfy, list_rule_not_satisfy


    def add_rule(self):

        
        body_data = request.get_json()
        _, id_user_login = get_data_by_decode()

        validate_rule = self.validate_add_rule(body_data)
        if validate_rule != False:
            return validate_rule


        if CommonKey.STATUS not in body_data:
            body_data[CommonKey.STATUS] = True
        rule = {
            CommonKey.NAME: body_data[CommonKey.NAME],
            CommonKey.STATUS: body_data[CommonKey.STATUS]
        }

        
        cretor = ObjectId(id_user_login)
        MGRule().create(rule, cretor)

        querry = {CommonKey.CREATE_BY: cretor}
        rule = MGRule().filter_one(querry)

        data = json.loads(json_util.dumps(rule))
        
        return response.success(data, "Thêm mới rule thành công")

    def get_all(self):

        token = request.headers['Authorization']
        data = jwt.decode(token, SECRET_KEY, algorithms=Authen.ALGORITHM)

        params = request.args
        validate_get_list_rule, page, perpage = self.validate_get_list_rule(params)
        if validate_get_list_rule != False:
            return validate_get_list_rule

        
        skip = (page-1) * perpage
        total_rule = MGRule().count_documents()
        total_page = math.ceil(total_rule / perpage)
        
        if (page == -1):
            skip = None
            perpage = None
            total_page = 1


        list_rule = MGRule().find(skip= skip, limit = perpage)
        data = {
            "total_page": total_page,
            "total_rule": total_rule,
            "list_rute": json.loads(json_util.dumps(list_rule)),
        }
        
        return response.success(data)
    
    def get_one(self,rule_id):
        
        validate_get_one_rule = self.validate_get_one_rule(rule_id)
        if validate_get_one_rule != False:
            return validate_get_one_rule

        querry = {"_id": ObjectId(rule_id)}
        rule = MGRule().filter_one(querry)
        data = json.loads(json_util.dumps(rule))

        
        return response.success(data)
    
    def change_status(self,rule_id, status):

        _, id_user_login = get_data_by_decode()

        validate_get_one_rule = self.validate_get_one_rule(rule_id)
        if validate_get_one_rule != False:
            return validate_get_one_rule
        
        querry = {"_id": ObjectId(rule_id)}
        payload = { CommonKey.STATUS: status }
        updater = ObjectId(id_user_login) # Fake updater

        MGRule().update_one(querry,payload,updater)

        rule = MGRule().filter_one(querry)
        data = json.loads(json_util.dumps(rule))

        return response.success(data)

    def disable_one(self,rule_id):
        return self.change_status(rule_id, False)
    
    def active_one(self,rule_id):
        return self.change_status(rule_id, True)
    
    def disable_list(self):
        body_data = request.get_json()

        list_rule_satisfy, list_rule_not_satisfy = self.validate_list_rule(body_data["id_list"])

        for rule_id in list_rule_satisfy:
            self.change_status(rule_id, False)
            
        data = {
            "list_id_success": list_rule_satisfy,
            "list_id_fail": list_rule_not_satisfy,
        }

        return response.success(data)
    


    


