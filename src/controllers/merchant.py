

from bson import ObjectId
from flask import Blueprint, request
from marshmallow import ValidationError
from src.models.mongo.merchant_db import MGMerchant

from src.models.schemas.merchant_schemas import MerchantSchema


merchant_url = Blueprint('merchant', __name__)

@merchant_url.route('', methods=['POST'])
def create_merchant():
    body = request.get_json()
    try:
        val_body = MerchantSchema().load(body)
    except ValidationError as err:
        return {"code": 400, "message": err.messages}, 400
    result = MGMerchant().create(payload=body, creator=ObjectId("6417c64a19514401d8230118"))
    
    del result["create_by"]
    del result["update_at"]
    del result["update_by"]
    
    return {"code": 200, 'data':result}