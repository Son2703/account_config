from flask import Blueprint, request
from src.apis import HTTP
from src.common.constants import Role
from src.helps.func import get_json_from_mongo
from src.models.mongo.user_db import MGUser


user_table = MGUser()

user_url = Blueprint('user', __name__)


@user_url.route('', methods=[HTTP.METHOD.GET])
def get_all():
    query = dict(request.args)
    query["fields"] = [v for v in query["fields"].split(',') if v] or []
    query["projection"] = {key: True for key in query["fields"]}

    users = user_table.find(
        {
            "role": {
                "$ne": Role.ADMIN.value
            }
        },
        skip=query["skip"], limit=query["limit"], projection=query["projection"])
    
    result = get_json_from_mongo(users)
    return list(result)
