from flask import Blueprint, request
from src.apis import *  
from src.controllers.rule.rule_controllers import RuleControllers          
from src.apis.uri import URI        
from src.auth.auth import token_required                                                                   

rule_service = Blueprint('rule_service', __name__, template_folder='templates')


@rule_service.route(URI.RULE.RULES, methods = [HTTP.METHOD.POST])
@token_required
def add_rule():
    return RuleControllers().add_rule()




@rule_service.route(URI.RULE.RULES, methods = [HTTP.METHOD.GET]) 
@token_required
def get_all():
    return RuleControllers().get_all()




@rule_service.route(URI.RULE.RULE_DETAIL, methods = [HTTP.METHOD.GET])
def get_one(rule_id):
    return RuleControllers().get_one(rule_id)



@token_required
@rule_service.route(URI.RULE.RULE_DISABLE_ONE_RULE, methods = [HTTP.METHOD.PATCH])
def disable_one(rule_id):
    return  RuleControllers().disable_one(rule_id)



@token_required
@rule_service.route(URI.RULE.RULE_ACTIVE_ONE_RULE, methods = [HTTP.METHOD.PATCH])
def active_one(rule_id):
    return  RuleControllers().active_one(rule_id)


@rule_service.route(URI.RULE.RULE_DISABLE_LIST_RULE, methods = [HTTP.METHOD.PATCH])
@token_required
def disable_list():
    return  RuleControllers().disable_list()