

from bson import ObjectId
from flask import Blueprint, request
from marshmallow import ValidationError
from src.auth.auth import create_access_token
from src.models.mongo.user_db import MGUser

from src.models.schemas.user_schemas import SignInSchema
from werkzeug.security import check_password_hash


root_url = Blueprint('root', __name__)

@root_url.route("/login", methods=["POST"])
def login():
    body = request.get_json()
    
    try:
        val_body = SignInSchema().load(body)
    except ValidationError as err:
        return {"code": 400, "message": err.messages}, 400
    
    val_body["id_merchant"] = ObjectId(val_body["id_merchant"])
    # val_body["password"] = check_password_hash(val_body["password"])
    print("AAASSDFSDFSDF", val_body, flush=True)
    current_user = MGUser().filter_one({
        "username": val_body["username"],
        "id_merchant": val_body["id_merchant"],
        "status": 1
    })

    if current_user is None:
        return {"code": 404, "message": "User not found!"}, 404

    match_password = check_password_hash(current_user["password"], val_body["password"])

    if not match_password:
        return {"code": 403, "message": "Login fail!"}, 403

    create_access_token(data=current_user, )
    print("LOGINNNNNNNN", current_user, flush=True)


    return "a"