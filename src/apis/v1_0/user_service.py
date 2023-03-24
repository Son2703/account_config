from flask import Blueprint    
from src.apis import *  
from src.controllers.user.user_controller import UserControllers          
from src.apis.uri import URI    
from src.auth.auth import token_required                                                                       

user_service = Blueprint('user_service', __name__, template_folder='templates')


@user_service.route(URI.USER.USERS, methods = [HTTP.METHOD.POST])
@token_required
def create():
    return UserControllers().create()

@user_service.route(URI.USER.CHANGE_PASS, methods = [HTTP.METHOD.PUT])
@token_required
def change_pass():
    return UserControllers().change_pass()

@user_service.route(URI.USER.DETAIL, methods = [HTTP.METHOD.GET])
@token_required
def get_user(id_user):
    return UserControllers().get_user(id_user)

@user_service.route(URI.USER.LOCK, methods=[HTTP.METHOD.PUT])
@token_required
def lock_user():
    return UserControllers().lock_user()

@user_service.route(URI.USER.DELETE, methods = [HTTP.METHOD.DELETE])
@token_required
def delete_user(id_user):
    return UserControllers().delete_user(id_user)

@user_service.route(URI.USER.BULK_INSERT_MANY, methods=[HTTP.METHOD.GET])
@token_required
def bulk_insert():
    return UserControllers().bulk_insert()