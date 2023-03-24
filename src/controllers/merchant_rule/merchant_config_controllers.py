from flask import Blueprint, request, jsonify
from src.models.mongo.merchant_cf_db import MGMerchantRuleAssignment
from src.models.schemas.merchant_config_schemas import *
from src.common.constants import Rule, Role
from src.common.message import Message
from src.common.common import CommonKey
from src.apis.v1_0 import *
from src.models.mongo.rule_db import MGRule
from src.common.time import timestamp_utc
from src.auth.auth import get_data_by_decode
from src.apis import *
from bson import json_util
import json
from mobio.sdks.base.common.mobio_exception import BaseMoError, DBLogicError, InputNotFoundError, LogicSystemError, \
    ParamInvalidError, CustomError, CustomUnauthorizeError, UnauthorizationError
import logging

import os, sys

class MerchantRuleControllers():


    @staticmethod
    def create():
        try:
            # id_merchant, id_user = get_data_by_decode()
            id_merchant = "asddwq3234sdadsaasddsdasd"

            data = MerchantConfigSchenma().load(request.json)
            current_config = MGMerchantRuleAssignment().find(
                payload={CommonKey.ID_MERCHANT: id_merchant})
            if current_config != []:
                # return conflict(Message.DATA_EXIST)
                pass
            MGMerchantRuleAssignment().delete_all()
            all_rules = MGRule().find({CommonKey.STATUS: True})
            all_rules = [{"_id": "1","name": "val_name"},
                            {"_id": "2","name": "val_pass"},
                            {"_id": "3","name": "change_pass_moth"},
                            {"_id": "4","name": "unique_old_pass"},
                            {"_id": "5","name": "require_change_pass"},
                            {"_id": "6","name": "unique_pass"},
                            {"_id": "7","name": "lock_account"}]
            all_name_rules = MerchantRuleControllers.find_names_rule(all_rules)
            # MGMerchantRuleAssignment().delete({CommonKey.ID_MERCHANT: id_merchant})
            payload = []
            for item in data:
                print(item, flush=True)
                if item not in all_name_rules:
                    # return conflict(InputNotFoundError("not_create_config"))
                    pass
                merchant_config = {CommonKey.ID_MERCHANT: id_merchant}
                if item == Rule.VAL_NAME.value:
                    values = ValNameSchema().load(data[Rule.VAL_NAME.value])
                    merchant_config.update({CommonKey.ID_RULE: MerchantRuleControllers.filter_id_rule(all_rules, Rule.VAL_NAME.value)})
                if item == Rule.VAL_PASS.value:
                    values = ValPassSchema().load(data[Rule.VAL_PASS.value])
                    merchant_config.update({CommonKey.ID_RULE: MerchantRuleControllers.filter_id_rule(all_rules, Rule.VAL_PASS.value)})
                if item == Rule.CHANGE_PASS_MOTH.value:
                    values = BaseValueSchema().load(
                        data[Rule.CHANGE_PASS_MOTH.value])
                    merchant_config.update({CommonKey.ID_RULE: MerchantRuleControllers.filter_id_rule(all_rules, Rule.CHANGE_PASS_MOTH.value)})
                if item == Rule.UNIQUE_OLD_PASS.value:
                    values = BaseValueSchema().load(
                        data[Rule.UNIQUE_OLD_PASS.value])
                    merchant_config.update({CommonKey.ID_RULE: MerchantRuleControllers.filter_id_rule(all_rules, Rule.UNIQUE_OLD_PASS.value)})
                if item == Rule.REQUIRE_CHANGE_PASS.value:
                    values = BaseCheckSchema().load(
                        data[Rule.REQUIRE_CHANGE_PASS.value])
                    merchant_config.update({CommonKey.ID_RULE: MerchantRuleControllers.filter_id_rule(all_rules, Rule.REQUIRE_CHANGE_PASS.value)})
                if item == Rule.UNIQUE_PASS.value:
                    values = BaseCheckSchema().load(
                        data[Rule.UNIQUE_PASS.value])
                    merchant_config.update({CommonKey.ID_RULE: MerchantRuleControllers.filter_id_rule(all_rules, Rule.UNIQUE_PASS.value)})
                if item == Rule.LOCK_ACCOUNT.value:
                    values = LockAccountSchema().load(
                        data[Rule.LOCK_ACCOUNT.value])
                    merchant_config.update({CommonKey.ID_RULE: MerchantRuleControllers.filter_id_rule(all_rules, Rule.LOCK_ACCOUNT.value)})
                merchant_config.update(values)
                payload.append(merchant_config)
            # data_update = MGMerchantRuleAssignment().create_many_config(payload, id_user)
            data_update = MGMerchantRuleAssignment().create_many_config(payload)
            print(data_update, flush=True)
            data.update({CommonKey.ID_MERCHANT: id_merchant})
            data.update(data_update)
        except Exception as e:
            print(e, flush=True)
        return build_response_message({"data": data})


    @staticmethod
    def get():
        try:
            # id_merchant, _ = get_data_by_decode()
            id_merchant = "asddwq3234sdadsaasddsdasd"
            data = MGMerchantRuleAssignment().find({CommonKey.ID_MERCHANT: id_merchant})
            if data == []:
                raise Exception("config of merchant not exist")
            # all_rules = MGRule().find({CommonKey.STATUS: True})
            result = MerchantRuleControllers.convert_merchant_config(data, id_merchant)
            print(result, flush=True)
            
        except Exception as e:
            print(e, flush=True)

        return build_response_message({"data": result})


    @staticmethod
    def update():
        try:
            # id_merchant, id_user = get_data_by_decode()
            id_merchant = "asddwq3234sdadsaasddsdasd"
            data = MerchantConfigSchenma().load(request.json)
            time_update = timestamp_utc()
            current_config = MGMerchantRuleAssignment().find(
                {CommonKey.ID_MERCHANT: id_merchant})
            if current_config == []:
                return not_found(Message.NOT_FOUND)
            keys = list(data.keys())
            for item in current_config:
                print(data.keys())
                value_update = ValNameSchema().load(
                    data[Rule.VAL_NAME.value]) if Rule.VAL_NAME.value in keys else {}
                value_update = ValPassSchema().load(
                    data[Rule.VAL_PASS.value]) if Rule.VAL_PASS.value in keys else {}
                value_update = BaseValueSchema().load(
                    data[Rule.CHANGE_PASS_MOTH.value]) if Rule.CHANGE_PASS_MOTH.value in keys else {}
                value_update = BaseValueSchema().load(
                    data[Rule.UNIQUE_OLD_PASS.value]) if Rule.UNIQUE_OLD_PASS.value in keys else {}
                value_update = BaseCheckSchema().load(
                    data[Rule.REQUIRE_CHANGE_PASS.value]) if Rule.REQUIRE_CHANGE_PASS.value in keys else {}
                value_update = BaseCheckSchema().load(
                    data[Rule.UNIQUE_PASS.value]) if Rule.UNIQUE_PASS.value in keys else {}
                value_update = LockAccountSchema().load(
                    data[Rule.LOCK_ACCOUNT.value]) if Rule.LOCK_ACCOUNT.value in keys else {}
                print("33333333333333")

                MGMerchantRuleAssignment().update_custom({CommonKey.ID_MERCHANT: item[CommonKey.ID_MERCHANT],
                                        CommonKey.ID_RULE: item[CommonKey.ID_RULE]}, value_update, "id_user", time_update)
            print("222222222222", flush=True)
            data.update({CommonKey.ID_MERCHANT: id_merchant})
            data.update({
                CommonKey.CREATE_BY: current_config[0][CommonKey.CREATE_BY],
                CommonKey.UPDATE_BY: "id_user",
                CommonKey.CREATE_AT: time_update,
                CommonKey.UPDATE_AT: current_config[0][CommonKey.CREATE_AT]
            })
            print(data, flush=True)
            print("11111111111", flush=True)
        except Exception as e:
            print(e, flush=True)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
        return build_response_message({"data": data})


    @staticmethod
    def delete():
        try:
            id_merchant, _ = get_data_by_decode()

            current_config = MGMerchantRuleAssignment().find(
                {CommonKey.ID_MERCHANT: id_merchant})
            if current_config == []:
                return not_found(Message.NOT_FOUND)
        except Exception as e:
            print(e, flush=True)
        return build_response_message({CommonKey.ID_MERCHANT: id_merchant})

    @staticmethod
    def convert_value(data):
        data.pop(CommonKey.ID_RULE)
        data.pop(CommonKey.ID)
        data.pop(CommonKey.ID_MERCHANT)
        data.pop(CommonKey.CREATE_AT)
        data.pop(CommonKey.CREATE_BY)
        data.pop(CommonKey.UPDATE_AT)
        data.pop(CommonKey.UPDATE_BY)
        return data
    
    @staticmethod
    def convert_merchant_config(data, id_merchant):
        result = {}
        result.update({  # Nguoi create, update. time create va time update cua config cac rule trong mot merchant la nhu nhau
            CommonKey.ID_MERCHANT: id_merchant,
            CommonKey.CREATE_AT: next(iter(data))[CommonKey.CREATE_AT],
            CommonKey.CREATE_BY: next(iter(data))[CommonKey.CREATE_BY],
            CommonKey.UPDATE_AT: next(iter(data))[CommonKey.UPDATE_AT],
            CommonKey.UPDATE_BY: next(iter(data))[CommonKey.UPDATE_BY],
        })
        all_rules = MGRule().find({CommonKey.STATUS: True})
        for item in data:
            element = {}
            if item[CommonKey.ID_RULE] == MerchantRuleControllers.filter_id_rule(all_rules, Rule.VAL_NAME.value):
                element[Rule.VAL_NAME.value] = item
            if item[CommonKey.ID_RULE] == MerchantRuleControllers.filter_id_rule(all_rules, Rule.VAL_PASS.value):
                element[Rule.VAL_PASS.value] = item
            if item[CommonKey.ID_RULE] == MerchantRuleControllers.filter_id_rule(all_rules, Rule.CHANGE_PASS_MOTH.value):
                element[Rule.CHANGE_PASS_MOTH.value] = item
            if item[CommonKey.ID_RULE] == MerchantRuleControllers.filter_id_rule(all_rules, Rule.UNIQUE_OLD_PASS.value):
                element[Rule.UNIQUE_OLD_PASS.value] = item
            if item[CommonKey.ID_RULE] == MerchantRuleControllers.filter_id_rule(all_rules, Rule.REQUIRE_CHANGE_PASS.value):
                element[Rule.REQUIRE_CHANGE_PASS.value] = item
            if item[CommonKey.ID_RULE] == MerchantRuleControllers.filter_id_rule(all_rules, Rule.UNIQUE_PASS.value):
                element[Rule.UNIQUE_PASS.value] = item
            if item[CommonKey.ID_RULE] == MerchantRuleControllers.filter_id_rule(all_rules, Rule.LOCK_ACCOUNT.value):
                element[Rule.LOCK_ACCOUNT.value] = item
            MerchantRuleControllers.convert_value(next(iter(list(element.values()))))
            result.update(element)
        return result

    @staticmethod
    def filter_id_rule(data, rule_name):
        for x in data:
            if x[CommonKey.NAME] == rule_name:
                return str(x[CommonKey.ID])
    
    @staticmethod 
    def find_names_rule(data):
        return [a[CommonKey.NAME] for a in data]
    