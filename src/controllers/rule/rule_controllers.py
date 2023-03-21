from flask import request,jsonify
from src.models.mongo.rule_model import RuleModel
from bson import ObjectId,json_util
from mobio.libs.logging import MobioLogging
from mobio.sdks.base.controllers import BaseController
from mobio.libs.validator import Required, InstanceOf, In
from src.common.constants import LIST_RULE_NAME
from mobio.libs.validator import Validator, HttpValidator, VALIDATION_RESULT, Length, Required, InstanceOf, In, Password, Pattern
import json
from src.apis import response
from src.common.common import is_ObjectID_valid



class RuleControllers(BaseController):
    def __init__(self):
        BaseController().__init__()

    def validate_add_rule(self, input_data):
        rule_validate = {
            "name": [Required, In(LIST_RULE_NAME)],
            "status": [InstanceOf(bool)]
        }

        valid = HttpValidator(rule_validate)
        val_result = valid.validate_object(input_data)
        
        if not val_result[VALIDATION_RESULT.VALID]:
            return response.bad_request(val_result[VALIDATION_RESULT.ERRORS])
        
        #Name already exists
        querry_name = {"name": input_data["name"]}
        if RuleModel().count_documents(querry_name) > 0:
            return response.bad_request("Rule đã có trong hệ thống")
        
        return False
    
    def validate_get_list_rule(self, page, perpage):

        # try: 
        #     int(page)
        
        #     return response.bad_request("Page phải là số  nguyên")
        
        # querry = {"_id": ObjectId(rule_id)}
        # if RuleModel().count_documents(querry) == 0:
        #     return response.bad_request("Perpage phải là số nguyên")

        return False
    
    def validate_get_one_rule(self, rule_id):

        if is_ObjectID_valid(rule_id) == False:
            return response.bad_request("ID không hợp lệ")
        
        querry = {"_id": ObjectId(rule_id)}
        if RuleModel().count_documents(querry) == 0:
            return response.bad_request("Rule không có trong hệ thống")

        return False


    def add_rule(self):
        body_data = request.get_json()

        validate_rule = self.validate_add_rule(body_data)
        if validate_rule != False:
            return validate_rule


        if "status" not in body_data:
            body_data["status"] = True
        rule = {
            "name": body_data["name"],
            "status": body_data["status"]
        }

        # Fake cretor
        cretor = ObjectId()

        RuleModel().create(rule, cretor)

        querry = {"create_by": cretor}
        rule = RuleModel().filter_one(querry)

        data = json.loads(json_util.dumps(rule))
        
        return response.success(data, "Thêm mới rule thành công")

    def get_all(self):
        try:
            page = int(request.args.get("page"))
            perpage = int(request.args.get("perpage"))
        except:
            return response.bad_request("Page, perpage phải là số nguyên")

        validate_get_list_rule = self.validate_get_list_rule(page,perpage)
        if validate_get_list_rule != False:
            return validate_get_list_rule

        
        skip = (page-1) * perpage
        total_rule = RuleModel().count_documents()
        total_page = total_rule // perpage + 1
        
        if (page == -1):
            skip = None
            perpage = None


        list_rule = RuleModel().find(skip= skip, limit = perpage)
        data = {
            "total_page": total_page,
            "total_rule": total_rule,
            "list_rute": json.loads(json_util.dumps(list_rule))
        }
        
        return response.success(data)
    
    def get_one(self,rule_id):
        
        validate_get_one_rule = self.validate_get_one_rule(rule_id)
        if validate_get_one_rule != False:
            return validate_get_one_rule

        querry = {"_id": ObjectId(rule_id)}
        rule = RuleModel().filter_one(querry)
        data = json.loads(json_util.dumps(rule))

        
        return response.success(data)
    


