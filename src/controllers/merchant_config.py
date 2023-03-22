from flask import Blueprint, request, jsonify
from src.models.mongo.merchant_cf_db import MGconfig
from src.models.schemas.merchant_config_schemas import *
from src.common.constants import Rule, Role
from src.common.common import CommonKey
from src.apis import HTTP
from src.common.time import timestamp_utc
from src.auth.auth import token_required


merchant_cf = Blueprint("config", __name__)



@merchant_cf.route('/configs', methods=[HTTP.METHOD.POST])
@token_required
def create(id_merchant):
    try:
        data = MerchantConfigSchenma().load(request.json)
        current_config = MGconfig().find(
            payload={CommonKey.ID_MERCHANT: id_merchant})
        if current_config != []:
            return jsonify("Data exist"), 409
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
    return jsonify({CommonKey.CODE: 200, CommonKey.DATA: MerchantConfigSchenma().load(result)}), 200



@merchant_cf.route('/configs', methods=[HTTP.METHOD.GET])
@token_required
def get_by_id(id_merchant):
    try:
        data = MGconfig().find({CommonKey.ID_MERCHANT: id_merchant})
        print(data, flush=True)
        if data == []:
            raise Exception("config of merchant not exist")
        else:
            result = find_merchant_config(data, id_merchant)
    except Exception as e:
        print(e, flush=True)

    return jsonify({CommonKey.CODE: 200, CommonKey.DATA: result}), 200

def convert_value(data):
    data.pop(CommonKey.ID_RULE)
    data.pop(CommonKey.ID)
    data.pop(CommonKey.ID_MERCHANT)
    data.pop(CommonKey.CREATE_AT)
    data.pop(CommonKey.CREATE_BY)
    data.pop(CommonKey.UPDATE_AT)
    data.pop(CommonKey.UPDATE_BY)
    return data

def find_merchant_config(data, id_merchant):
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
        convert_value(list(element.values())[0])
        result.update(element)
    return result



@merchant_cf.route('/configs', methods=[HTTP.METHOD.PUT])
@token_required
def update(id_merchant):
    try:
        data = MerchantConfigSchenma().load(request.json)
        time_update = timestamp_utc()
        current_config = MGconfig().find(
            {CommonKey.ID_MERCHANT: id_merchant})
        if current_config == []:
            raise Exception("config of merchant not exist")
        for item in current_config:

            value_update = {CommonKey.SET: ValNameSchema().load(
                data[Rule.VAL_NAME.value])} if Rule.VAL_NAME.value in data.keys else {CommonKey.SET: {}}
            value_update = {CommonKey.SET: ValPassSchema().load(
                data[Rule.VAL_PASS.value])} if Rule.VAL_PASS.value in data.keys else {CommonKey.SET: {}}
            value_update = {CommonKey.SET: BaseValueSchema().load(
                data[Rule.CHANGE_PASS_MOTH.value])} if Rule.CHANGE_PASS_MOTH.value in data.keys else {CommonKey.SET: {}}
            value_update = {CommonKey.SET: BaseValueSchema().load(
                data[Rule.UNIQUE_OLD_PASS.value])} if Rule.UNIQUE_OLD_PASS.value in data.keys else {CommonKey.SET: {}}
            value_update = {CommonKey.SET: BaseCheckSchema().load(
                data[Rule.REQUIRE_CHANGE_PASS.value])} if Rule.REQUIRE_CHANGE_PASS.value in data.keys else {CommonKey.SET: {}}
            value_update = {CommonKey.SET: BaseCheckSchema().load(
                data[Rule.UNIQUE_PASS.value])} if Rule.UNIQUE_PASS.value in data.keys else {CommonKey.SET: {}}
            value_update = {CommonKey.SET: LockAccountSchema().load(
                data[Rule.LOCK_ACCOUNT.value])} if Rule.LOCK_ACCOUNT.value in data.keys else {CommonKey.SET: {}}

            MGconfig().update_custom({CommonKey.ID_MERCHANT: item[CommonKey.ID_MERCHANT],
                                      CommonKey.ID_RULE: item[CommonKey.ID_RULE]}, value_update, Role.ADMIN.value, time_update)
    except Exception as e:
        print(e, flush=True)
    return jsonify({CommonKey.CODE: 200, CommonKey.DATA: data}), 200



@merchant_cf.route('/configs', methods=[HTTP.METHOD.DELETE])
def delete():
    try:
        MGconfig().delete_all()
    except Exception as e:
        print(e, flush=True)
    return jsonify({CommonKey.CODE: 200}), 200
