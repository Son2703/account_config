from flask import Blueprint    
from src.apis import *  
from src.controllers.user.user_controller import UserControllers          
from src.apis.uri import URI                                                                           

user_service = Blueprint('user_service', __name__, template_folder='templates')


@user_service.route(URI.USER.USERS, methods = [HTTP.METHOD.POST])
def Register():
    return UserControllers().Register()

@user_service.route(URI.USER.USER_CHANGEPASS, methods = [HTTP.METHOD.PUT])
def ChangePass(user_id):
    return UserControllers().ChangePass(user_id)

@user_service.route(URI.USER.USER_DETAIL, methods = [HTTP.METHOD.GET])
def GetUser(user_id):
    return UserControllers().GetUser(user_id)

@user_service.route(URI.USER.USER_LOCK, methods=[HTTP.METHOD.PUT])
def LockUser():
    return UserControllers().LockUser()


