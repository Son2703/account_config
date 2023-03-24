from flask import Blueprint    
from src.apis import *  
from src.controllers.user.user_controller import UserControllers          
from src.apis.uri import URI                                                                           

user_service = Blueprint('user_service', __name__, template_folder='templates')


@user_service.route(URI.USER.USERS, methods = [HTTP.METHOD.POST])
def register():
    print("2222222", flush=True)
    return UserControllers().register()

@user_service.route(URI.USER.USER_CHANGEPASS, methods = [HTTP.METHOD.PUT])
def change_pass(user_id):
    return UserControllers().change_pass(user_id)

@user_service.route(URI.USER.USER_DETAIL, methods = [HTTP.METHOD.GET])
def get_user(user_id):
    return UserControllers().get_user(user_id)

@user_service.route(URI.USER.USER_LOCK, methods=[HTTP.METHOD.PUT])
def lock_user():
    return UserControllers().lock_user()

@user_service.route(URI.USER.USER_DELETE, methods = [HTTP.METHOD.DELETE])
def delete_user(user_id):
    return UserControllers().delete_user(user_id)

@user_service.route(URI.USER.USER_BULK_INSERT_MANY, methods=[HTTP.METHOD.GET])
def bulk_insert():
    return UserControllers().bulk_insert()

@user_service.route(URI.USER.USER_BULK_INSERT_MANY_EXCEL, methods=[HTTP.METHOD.GET])
def excel_insert():
    return UserControllers().excel_insert()
