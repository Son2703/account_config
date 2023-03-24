
from src.models.mongo.rule_db import MGRule
from bson import ObjectId

from mobio.libs.validator import Required, InstanceOf, In
from src.common.constants import LIST_RULE_NAME
from mobio.libs.validator import HttpValidator, VALIDATION_RESULT, Required, InstanceOf, In
from src.apis import response
from src.common.common import is_ObjectID_valid
from src.common.common import CommonKey
from src.apis import *
from mobio.sdks.base.common.mobio_exception import BaseMoError

class ValidateRule():
    def validate_add_rule(input_data):
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
            return bad_request(BaseMoError("already_exist", CommonKey.RULE, input_data[CommonKey.NAME]))
        
        return False
    
    def validate_get_list_rule(params):
        
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
            return bad_request(BaseMoError("bad_request_page_perpage")), None, None
    
        return False, page, perpage
    
    def validate_get_one_rule(rule_id):

        if is_ObjectID_valid(rule_id) == False:
            return bad_request(BaseMoError("invalid_id"))
        
        querry = {"_id": ObjectId(rule_id)}
        if MGRule().count_documents(querry) == 0:
            return bad_request(BaseMoError("not_exist", CommonKey.RULE, rule_id))

        return False
    
    @classmethod
    def validate_list_rule(cls,list_rule):
        list_rule_satisfy = []
        list_rule_not_satisfy = []

        for rule_id in list_rule:
            if (cls.validate_get_one_rule(rule_id) == False):
                list_rule_satisfy.append(rule_id)
            else:
                list_rule_not_satisfy.append(rule_id)
        
        return list_rule_satisfy, list_rule_not_satisfy