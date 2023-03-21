from flask import Blueprint    
from src.apis import *  
from src.controllers.rule.rule_controllers import RuleControllers          
from src.apis.uri import URI                                                                           

rule_service = Blueprint('rule_service', __name__, template_folder='templates')


@rule_service.route(URI.RULE.RULES, methods = [HTTP.METHOD.POST])
def add_rule():
    return RuleControllers().add_rule()

@rule_service.route(URI.RULE.RULES, methods = [HTTP.METHOD.GET]) 
def get_all():
    return RuleControllers().get_all()

@rule_service.route(URI.RULE.RULE_DETAIL, methods = [HTTP.METHOD.GET])
def get_one(rule_id):
    return RuleControllers().get_one(rule_id)

# @rule_service.route("/rules", methods = [HTTP.METHOD.PATCH])
# def add_rule():
#     return build_response_message(RuleControllers().add_rule())

# @rule_service.route("/rules", methods = [HTTP.METHOD.PATCH])
# def add_rule():
#     return build_response_message(RuleControllers().add_rule())