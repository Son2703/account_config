from bson import ObjectId

class CommonKey:
    #Base
    CREATE_AT = "create_at"
    UPDATE_AT = "update_at"
    CREATE_BY = "create_by"
    UPDATE_BY = "update_by"


def is_ObjectID_valid(oid):
    if ObjectId.is_valid(oid):
        return True
    else:
        return False