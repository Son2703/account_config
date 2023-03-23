from flask import Blueprint, request, jsonify
from src.models.mongo.merchant_cf_db import MGconfig
from src.models.schemas.merchant_config_schemas import *
from src.common.constants import Rule, Role
from src.common.message import Message
from src.common.common import CommonKey
from src.apis.v1_0 import *
from src.common.time import timestamp_utc
from src.auth.auth import get_data_by_decode
from src.apis import *


class MerchantRuleControllers():

    @staticmethod
    def create():
        try:
            id_merchant, _ = get_data_by_decode()

            data = MerchantConfigSchenma().load(request.json)
            current_config = MGconfig().find(
                payload={CommonKey.ID_MERCHANT: id_merchant})
            if current_config != []:
                return conflict(Message.DATA_EXIST)
            else:
                payload = []
                for item in data:
                    merchant_config = {CommonKey.ID_MERCHANT: id_merchant}
                    if item == Rule.VAL_NAME.value:
                        values = ValNameSchema().load(data[Rule.VAL_NAME.value])
                        merchant_config.update({CommonKey.ID_RULE: "1"})
                    if item == Rule.VAL_PASS.value:
                        values = ValPassSchema().load(data[Rule.VAL_PASS.value])
                        merchant_config.update({CommonKey.ID_RULE: "2"})
                    if item == Rule.CHANGE_PASS_MOTH.value:
                        values = BaseValueSchema().load(
                            data[Rule.CHANGE_PASS_MOTH.value])
                        merchant_config.update({CommonKey.ID_RULE: "3"})
                    if item == Rule.UNIQUE_OLD_PASS.value:
                        values = BaseValueSchema().load(
                            data[Rule.UNIQUE_OLD_PASS.value])
                        merchant_config.update({CommonKey.ID_RULE: "4"})
                    if item == Rule.REQUIRE_CHANGE_PASS.value:
                        values = BaseCheckSchema().load(
                            data[Rule.REQUIRE_CHANGE_PASS.value])
                        merchant_config.update({CommonKey.ID_RULE: "5"})
                    if item == Rule.UNIQUE_PASS.value:
                        values = BaseCheckSchema().load(
                            data[Rule.UNIQUE_PASS.value])
                        merchant_config.update({CommonKey.ID_RULE: "6"})
                    if item == Rule.LOCK_ACCOUNT.value:
                        values = LockAccountSchema().load(
                            data[Rule.LOCK_ACCOUNT.value])
                        merchant_config.update({CommonKey.ID_RULE: "7"})
                    merchant_config.update(values)
                    payload.append(merchant_config)
                result = MGconfig().create_many(payload)
        except Exception as e:
            print(e, flush=True)
        return build_response_message(MerchantConfigSchenma().load(result))


    @staticmethod
    def get():
        try:
            id_merchant, _ = get_data_by_decode()

            data = MGconfig().find({CommonKey.ID_MERCHANT: id_merchant})
            if data == []:
                raise Exception("config of merchant not exist")
            else:
                result = MerchantRuleControllers.convert_merchant_config(data, id_merchant)
        except Exception as e:
            print(e, flush=True)

        return build_response_message(result)

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
            CommonKey.CREATE_AT: data[0][CommonKey.CREATE_AT],
            CommonKey.CREATE_BY: data[0][CommonKey.CREATE_BY],
            CommonKey.UPDATE_AT: data[0][CommonKey.UPDATE_AT],
            CommonKey.UPDATE_BY: data[0][CommonKey.UPDATE_BY],
        })
        for item in data:
            element = {}
            if item[CommonKey.ID_RULE] == "1":
                element[Rule.VAL_NAME.value] = item
            if item[CommonKey.ID_RULE] == "2":
                element[Rule.VAL_PASS.value] = item
            if item[CommonKey.ID_RULE] == '3':
                element[Rule.CHANGE_PASS_MOTH.value] = item
            if item[CommonKey.ID_RULE] == "4":
                element[Rule.UNIQUE_OLD_PASS.value] = item
            if item[CommonKey.ID_RULE] == "5":
                element[Rule.REQUIRE_CHANGE_PASS.value] = item
            if item[CommonKey.ID_RULE] == "6":
                element[Rule.UNIQUE_PASS.value] = item
            if item[CommonKey.ID_RULE] == "7":
                element[Rule.LOCK_ACCOUNT.value] = item
            MerchantRuleControllers.convert_value(list(element.values())[0])
            result.update(element)
        return result


    @staticmethod
    def update():
        try:
            id_merchant, id_user = get_data_by_decode()

            data = MerchantConfigSchenma().load(request.json)
            time_update = timestamp_utc()
            current_config = MGconfig().find(
                {CommonKey.ID_MERCHANT: id_merchant})
            if current_config == []:
                return not_found(Message.NOT_FOUND)
            for item in current_config:
                value_update = ValNameSchema().load(
                    data[Rule.VAL_NAME.value]) if Rule.VAL_NAME.value in data.keys else {}
                value_update = ValPassSchema().load(
                    data[Rule.VAL_PASS.value]) if Rule.VAL_PASS.value in data.keys else {}
                value_update = BaseValueSchema().load(
                    data[Rule.CHANGE_PASS_MOTH.value]) if Rule.CHANGE_PASS_MOTH.value in data.keys else {}
                value_update = BaseValueSchema().load(
                    data[Rule.UNIQUE_OLD_PASS.value]) if Rule.UNIQUE_OLD_PASS.value in data.keys else {}
                value_update = BaseCheckSchema().load(
                    data[Rule.REQUIRE_CHANGE_PASS.value]) if Rule.REQUIRE_CHANGE_PASS.value in data.keys else {}
                value_update = BaseCheckSchema().load(
                    data[Rule.UNIQUE_PASS.value]) if Rule.UNIQUE_PASS.value in data.keys else {}
                value_update = LockAccountSchema().load(
                    data[Rule.LOCK_ACCOUNT.value]) if Rule.LOCK_ACCOUNT.value in data.keys else {}

                MGconfig().update_custom({CommonKey.ID_MERCHANT: item[CommonKey.ID_MERCHANT],
                                        CommonKey.ID_RULE: item[CommonKey.ID_RULE]}, value_update, id_user, time_update)
            data.update({
                CommonKey.CREATE_BY: current_config[0][CommonKey.CREATE_BY],
                CommonKey.UPDATE_BY: id_user,
                CommonKey.CREATE_AT: time_update,
                CommonKey.UPDATE_AT: current_config[0][CommonKey.CREATE_AT]
            })
        except Exception as e:
            print(e, flush=True)
        return build_response_message(data)


    @staticmethod
    def delete_all():
        try:
            MGconfig().delete_all()
        except Exception as e:
            print(e, flush=True)
        return build_response_message({"status: success"})
    
    @staticmethod
    def delete():
        try:
            id_merchant, _ = get_data_by_decode()

            current_config = MGconfig().find(
                {CommonKey.ID_MERCHANT: id_merchant})
            if current_config == []:
                return not_found(Message.NOT_FOUND)
            MGconfig().delete({CommonKey.ID_MERCHANT: id_merchant})
        except Exception as e:
            print(e, flush=True)
        return build_response_message({CommonKey.ID_MERCHANT: id_merchant})
