from src.models.mongo.rule_db import MGRule
from src.models.mongo.merchant_cf_db import MGMerchantRuleAssignment
from src.models.mongo.list_pass_user_db import MGListPassUser
from src.common.constants import *
from src.common.message import Message
from src.common.common import *
from src.apis import *
from flask import jsonify


class FilterGroup():

    @staticmethod
    def number(a):
        if a.isdigit():
            return a

    @staticmethod
    def special_charater(a):
        if not a.isalnum():
            return a
        
    @staticmethod
    def upper(a):
        if a.isupper():
            return a

    @staticmethod
    def lowecase(a):
        if a.islower():
            return a

    staticmethod
    def filter_character(value, filter_group):
        a = filter(filter_group, value)
        return len((list(a)))
        

class RuleAuth():

    @staticmethod
    def need_change_password_first(user_info: dict):
        rule = MGRule().filter_one({"name": Rule.REQUIRE_CHANGE_PASS.value})
        # check rule is active
        if not rule:
            return
        if not rule["status"]:
            return

        # check config is active
        config = MGMerchantRuleAssignment().filter_one(
            {"id_rule": rule["_id"], "id_merchant": user_info["id_merhcnat"]})
        if not config:
            return
        if not config["status"]:
            return

        password_list_length = MGListPassUser().find().count_documents()
        if password_list_length != 1:
            return
        return True

    @staticmethod
    def validate_name(name, id_merchant):
        rule = MGRule().filter_one({CommonKey.NAME: Rule.VAL_NAME.value})
        config = MGMerchantRuleAssignment().filter_one(
            {CommonKey.ID_MERCHANT: ObjectId(id_merchant), CommonKey.ID_RULE: rule[CommonKey.ID]})
        if len(name) < config[CommonKey.MIN_LEN]:
            return unprocessable_content(BaseMoError(Message.MIN_LEN_ERROR, str(config[CommonKey.MIN_LEN])))

        if len(name) > config[CommonKey.MAX_LEN]:
            return unprocessable_content(BaseMoError(Message.MAX_LEN_ERROR, str(config[CommonKey.MAX_LEN])))
        if bool(config[CommonKey.ALL][CommonKey.CHECK]):
            number = config[CommonKey.ALL][CommonKey.NUMBER]
            special_character = config[CommonKey.ALL][CommonKey.SPECIAL_CHARACTER]
            if bool(number[CommonKey.CHECK]):
                number_in_name = FilterGroup.filter_character(
                    name, FilterGroup.number)
                if number_in_name < number[CommonKey.VALUE]:
                    return unprocessable_content(BaseMoError(Message.MIN_CHARACTER_ERROR, str(number[CommonKey.VALUE]), CommonKey.NUMBER, CommonKey.NAME))
            if bool(special_character[CommonKey.CHECK]):
                special_in_name = FilterGroup.filter_character(
                    name, FilterGroup.special_charater)
                if special_in_name < special_character[CommonKey.VALUE]:
                    return unprocessable_content(BaseMoError(Message.MIN_CHARACTER_ERROR, str(special_character[CommonKey.VALUE]), "dac biet", CommonKey.NAME))
        if bool(config[CommonKey.AT_LEAST][CommonKey.CHECK]):
            number = config[CommonKey.AT_LEAST][CommonKey.NUMBER]
            special_character = config[CommonKey.AT_LEAST][CommonKey.SPECIAL_CHARACTER]
            if bool(config[CommonKey.AT_LEAST][CommonKey.VALUE]):
                check = 0
                count = 0
                if bool(number[CommonKey.CHECK]):
                    check += 1
                    number_in_name = FilterGroup.filter_character(
                        name, FilterGroup.number)
                    if number_in_name < number[CommonKey.VALUE]:
                        count += 1
                if bool(special_character[CommonKey.CHECK]):
                    check += 1
                    special_in_name = FilterGroup.filter_character(
                        name, FilterGroup.special_charater)
                    if special_in_name < special_character[CommonKey.VALUE]:
                        count += 1
                if config[CommonKey.AT_LEAST][CommonKey.VALUE] == check and bool(count):
                    return unprocessable_content(BaseMoError((Message.FIELD_CHARACTER_ERROR, CommonKey.NAME)))
                if count > config[CommonKey.AT_LEAST][CommonKey.VALUE]:
                    return unprocessable_content(BaseMoError((Message.FIELD_CHARACTER_ERROR, CommonKey.NAME)))
        return False
    
    @staticmethod
    def validate_pass(password, id_merchant):
        rule = MGRule().filter_one({CommonKey.NAME: Rule.VAL_PASS.value})
        config = MGMerchantRuleAssignment().filter_one(
            {CommonKey.ID_MERCHANT: ObjectId(id_merchant), CommonKey.ID_RULE: rule[CommonKey.ID]})
        if len(password) < config[CommonKey.MIN_LEN]:
            return unprocessable_content(BaseMoError(Message.MIN_LEN_ERROR, str(config[CommonKey.MIN_LEN])))

        if len(password) > config[CommonKey.MAX_LEN]:
            return unprocessable_content(BaseMoError(Message.MAX_LEN_ERROR, str(config[CommonKey.MAX_LEN])))

        if bool(config[CommonKey.ALL][CommonKey.CHECK]):
            number = config[CommonKey.ALL][CommonKey.NUMBER]
            special_character = config[CommonKey.ALL][CommonKey.NUMBER]
            upper = config[CommonKey.ALL][CommonKey.UPPER]
            lower = config[CommonKey.ALL][CommonKey.LOWECASE]

            if bool(number[CommonKey.CHECK]):
                number_in_pass = FilterGroup.filter_character(
                    password, FilterGroup.number)
                if number_in_pass < number[CommonKey.VALUE]:
                    return unprocessable_content(BaseMoError(Message.MIN_CHARACTER_ERROR, str(number[CommonKey.VALUE]), CommonKey.NUMBER, CommonKey.PASSWORD))

            if bool(special_character[CommonKey.CHECK]):
                special_in_pass = FilterGroup.filter_character(
                    password, FilterGroup.special_charater)
                if special_in_pass < special_character[CommonKey.VALUE]:
                    return unprocessable_content(BaseMoError(Message.MIN_CHARACTER_ERROR, str(special_character[CommonKey.VALUE]), CommonKey.SPECIAL_CHARACTER, CommonKey.PASSWORD))
            
            if bool(upper[CommonKey.CHECK]):
                upper_in_pass = FilterGroup.filter_character(
                    password, FilterGroup.special_charater)
                if upper_in_pass < upper[CommonKey.VALUE]:
                    return unprocessable_content(BaseMoError(Message.MIN_CHARACTER_ERROR, str(upper[CommonKey.VALUE]), CommonKey.UPPER, CommonKey.PASSWORD))
                
            if bool(lower[CommonKey.CHECK]):
                lower_in_pass = FilterGroup.filter_character(
                    password, FilterGroup.special_charater)
                if lower_in_pass < lower[CommonKey.VALUE]:
                    return unprocessable_content(BaseMoError(Message.MIN_CHARACTER_ERROR, str(lower[CommonKey.VALUE]), CommonKey.LOWECASE, CommonKey.PASSWORD))

        if bool(config[CommonKey.AT_LEAST][CommonKey.CHECK]):
            number = config[CommonKey.AT_LEAST][CommonKey.NUMBER]
            special_character = config[CommonKey.AT_LEAST][CommonKey.SPECIAL_CHARACTER]
            upper = config[CommonKey.AT_LEAST][CommonKey.UPPER]
            lower = config[CommonKey.AT_LEAST][CommonKey.LOWECASE]
            if bool(config[CommonKey.AT_LEAST][CommonKey.VALUE]):
                check = 0
                count = 0
                if bool(number[CommonKey.CHECK]):
                    check += 1
                    number_in_pass = FilterGroup.filter_character(
                        password, FilterGroup.number)
                    if number_in_pass < number[CommonKey.VALUE]:
                        count += 1
                if bool(special_character[CommonKey.CHECK]):
                    check += 1
                    special_in_pass = FilterGroup.filter_character(
                        password, FilterGroup.special_charater)
                    if special_in_pass < special_character[CommonKey.VALUE]:
                        count += 1
                if bool(upper[CommonKey.CHECK]):
                    check += 1
                    upper_in_pass = FilterGroup.filter_character(
                        password, FilterGroup.upper)
                    if upper_in_pass < upper[CommonKey.VALUE]:
                        count += 1
                if bool(lower[CommonKey.CHECK]):
                    check += 1
                    lower_in_pass = FilterGroup.filter_character(
                        password, FilterGroup.lowecase)
                    if lower_in_pass < lower[CommonKey.VALUE]:
                        count += 1
                if config[CommonKey.AT_LEAST][CommonKey.VALUE] == check and bool(count):
                    return unprocessable_content(BaseMoError((Message.FIELD_CHARACTER_ERROR, CommonKey.PASSWORD)))
                if count > config[CommonKey.AT_LEAST][CommonKey.VALUE]:
                    return unprocessable_content(BaseMoError((Message.FIELD_CHARACTER_ERROR, CommonKey.PASSWORD)))
        return False
