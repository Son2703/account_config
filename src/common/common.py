from bson import ObjectId

class CommonKey:
    #Base
    CREATE_AT = "create_at"
    UPDATE_AT = "update_at"
    CREATE_BY = "create_by"
    UPDATE_BY = "update_by"
    PAGE      = "page"
    PERPAGE   = "perpage"


    ID = "_id"

    #Merchant
    ID_MERCHANT = "id_merchant"

    #Rule
    ID_RULE = "id_rule"
    NAME= "name"

    #result
    CODE = "code"
    DATA = "data"

    #mongo
    SET = "$set"

    #user
    ID_USER = "id_user"
    USERNAME = "username"
    PASSWORD = "password"
    STATUS = "status"
    LAST_LOGIN = "last_login"
    LOGIN_FAIL_NUMBER = "login_fail_number"
    
    #validator
    NEW_PASSWORD = "new_password"
    PASSWORD_CONFIRM = "password_confirm"






def is_ObjectID_valid(oid):
    if ObjectId.is_valid(oid):
        return True
    else:
        return False
