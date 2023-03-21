from flask import Blueprint    
from src.apis import *  
from src.controllers.user.user_controller import UserControllers          
from src.apis.uri import URI                                                                           

user_service = Blueprint('user_service', __name__, template_folder='templates')


@user_service.route(URI.USER.USERS, methods = [HTTP.METHOD.POST])
def add_rule():
    return UserControllers().add_user()


