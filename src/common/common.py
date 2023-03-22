from bson import ObjectId

class CommonKey:
    #Base
    CREATE_AT = "create_at"
    UPDATE_AT = "update_at"
    CREATE_BY = "create_by"
    UPDATE_BY = "update_by"


    ID = "_id"

    #Merchant
    ID_MERCHANT = "id_merchant"

    #Rule
    ID_RULE = "id_rule"

    #result
    CODE = "code"
    DATA = "data"

    #mongo
    SET = "$set"

    #user
    ID_USER = "id_user"
    USERNAME = "username"
    PASSWORD = 'password'
    STATUS = "status"






def is_ObjectID_valid(oid):
    if ObjectId.is_valid(oid):
        return True
    else:
        return False