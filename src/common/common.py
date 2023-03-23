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

    #Rule field
    ID_RULE = "id_rule"
    MIN_LEN = "min_len"
    MAX_LEN = "max_len"
    ALL = "all"
    AT_LEAST = "at_least"
    CHECK = "check"
    VALUE = "value"
    NUMBER = "number"
    SPECIAL_CHARACTER = "special_character"
    UPPER = "upper"
    LOWECASE = "lowecase"
    

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
