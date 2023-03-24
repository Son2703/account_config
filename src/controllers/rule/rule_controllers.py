from flask import request,jsonify
from src.models.mongo.rule_db import MGRule
from bson import ObjectId,json_util

from src.common.common import CommonKey
import math, jwt, json
from configs.base import SECRET_KEY
from configs.configs import Authen
from src.auth.auth import get_data_by_decode
from src.apis import *
from src.controllers.rule.rule_validator import ValidateRule as validate


class RuleControllers():
    def __init__(self):
        pass
    
    def add_rule(self):


        body_data = request.get_json()

        _, id_user_login = get_data_by_decode()

        validate_rule = validate.validate_add_rule(body_data)
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
        
        return response_message(data)

    def get_all(self):

        token = request.headers['Authorization']
        data = jwt.decode(token, SECRET_KEY, algorithms=Authen.ALGORITHM)

        params = request.args
        validate_get_list_rule, page, perpage = validate.validate_get_list_rule(params)
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
        
        return response_message(data)
    
    def get_one(self,rule_id):
        
        validate_get_one_rule = validate.validate_get_one_rule(rule_id)
        if validate_get_one_rule != False:
            return validate_get_one_rule

        querry = {"_id": ObjectId(rule_id)}

        rule = MGRule().filter_one(querry)

        data = json.loads(json_util.dumps(rule))

        
        return response_message(data)
    
    def change_status(self,rule_id, status):

        _, id_user_login = get_data_by_decode()

        validate_get_one_rule = validate.validate_get_one_rule(rule_id)
        if validate_get_one_rule != False:
            return validate_get_one_rule
        
        querry = {"_id": ObjectId(rule_id)}
        payload = { CommonKey.STATUS: status }
        updater = ObjectId(id_user_login) # Fake updater

        MGRule().update_one(querry,payload,updater)

        rule = MGRule().filter_one(querry)
        data = json.loads(json_util.dumps(rule))

        return response_message(data)

    def disable_one(self,rule_id):
        return self.change_status(rule_id, False)
    
    def active_one(self,rule_id):
        return self.change_status(rule_id, True)
    
    def disable_list(self):
        body_data = request.get_json()

        list_rule_satisfy, list_rule_not_satisfy = validate.validate_list_rule(body_data["id_list"])

        for rule_id in list_rule_satisfy:
            self.change_status(rule_id, False)
            
        data = {
            "list_id_success": list_rule_satisfy,
            "list_id_fail": list_rule_not_satisfy,
        }

        return response_message(data)
    


    


