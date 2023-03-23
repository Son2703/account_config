from flask import Blueprint
from src.apis import HTTP
from src.auth.auth import token_required
from src.controllers.merchant_rule.merchant_config_controllers import MerchantRuleControllers


merchant_role = Blueprint("config", __name__)

@merchant_role.route('/configs', methods=[HTTP.METHOD.POST])
@token_required
def create_config():
    return MerchantRuleControllers.create()

@merchant_role.route('/configs', methods=[HTTP.METHOD.GET])
@token_required
def get_config():
    return MerchantRuleControllers.get()

@merchant_role.route('/configs', methods=[HTTP.METHOD.PUT])
@token_required
def update_config():
    return MerchantRuleControllers.update()

@merchant_role.route('/configs', methods=[HTTP.METHOD.DELETE])
@token_required
def delete_all_configs():
    return MerchantRuleControllers.delete()

