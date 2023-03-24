from src.models.mongo.rule_db import MGRule
from src.models.mongo.merchant_cf_db import MGMerchantRuleAssignment
from src.models.mongo.list_pass_user_db import MGListPassUser
from src.common.constants import Rule
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
        config = MGMerchantRuleAssignment().filter_one(
            {CommonKey.ID_MERCHANT: id_merchant, CommonKey.ID_RULE: "1"})
        if len(name) < config[CommonKey.MIN_LEN]:
            return f"the minimum length of the name is not enough, {config[CommonKey.MIN_LEN]} character", 422

        if len(name) > config[CommonKey.MAX_LEN]:
            return f"exceeds the specified length {config[CommonKey.MAX_LEN]}, please enter again", 422

        if bool(config[CommonKey.ALL][CommonKey.CHECK]):
            number = config[CommonKey.ALL][CommonKey.NUMBER]
            special_character = config[CommonKey.ALL][CommonKey.NUMBER]

            if bool(number[CommonKey.CHECK]):
                number_in_name = FilterGroup.filter_character(
                    name, FilterGroup.number)
                if number_in_name < number[CommonKey.VALUE]:
                    return f"need {number[CommonKey.VALUE]} numeric characters in the name", 422

            if bool(special_character[CommonKey.CHECK]):
                special_in_name = FilterGroup.filter_character(
                    name, FilterGroup.special_charater)
                if special_in_name < special_character[CommonKey.VALUE]:
                    return f"requires {special_character[CommonKey.VALUE]} special characters in the name", 422

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
                    return "invalid name", 422
                if count > config[CommonKey.AT_LEAST][CommonKey.VALUE]:
                    return "invalid name", 422
        return True
