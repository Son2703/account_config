

from bson import ObjectId
from flask import Blueprint, request
from marshmallow import ValidationError
from src.helps.func import get_json_from_db, get_str_from_id
from src.models.mongo.merchant_db import MGMerchant

from src.models.schemas.merchant_schemas import MerchantSchema

merchant_table = MGMerchant()

merchant_url = Blueprint('merchant', __name__)


@merchant_url.route('', methods=['POST'])
def create_merchant():
    body = request.get_json()
    try:
        val_body = MerchantSchema().load(body)
    except ValidationError as err:
        return {"code": 400, "message": err.messages}, 400
    result = merchant_table.create(
        payload=body, creator=ObjectId("6417c64a19514401d8230118"))
    result = get_json_from_db({
        # "id": result.inserted_id,
        **result
    })
    # del result["create_by"]
    # del result["update_at"]
    # del result["update_by"]

    return {"code": 200, 'data': result}


@merchant_url.route('/<id>', methods=['PUT'])
def update_merchant(id: int):

    if not id or not ObjectId().is_valid(id):
            return {"code": 400, "message": "invalid ID"}, 400

    body = request.get_json()
    current_merchant = merchant_table.filter_one(
        {"_id": ObjectId(id)},
        {"_id": False}
    )
    if current_merchant is None:
        return {"code": 404, "message": "Merchant not found!"}, 404

    try:
        val_body = MerchantSchema().load(body)
    except ValidationError as err:
        return {"code": 400, "message": err.messages}, 400

    val_body = {**current_merchant, **val_body}
    result = merchant_table.update_one(
        query={"_id": ObjectId(id)},
        payload=val_body, updater=ObjectId("6417c64a19514401d8230118"))
    result = get_json_from_db({
        **result
    })
    # del result["create_by"]
    # del result["update_at"]
    # del result["update_by"]

    return {"code": 200, 'data': result}


@merchant_url.route('/<id>', methods=["GET"])
def get_one(id: int):
    if not id or not ObjectId().is_valid(id):
        return {"code": 400, "message": "invalid ID"}, 400

    merchant = merchant_table.filter_one({"_id": ObjectId(id)})

    if not merchant:
        return {"code": 404, "message": "Merchant not found!"}, 404

    merchant["id"] = merchant.pop("_id")
    return get_json_from_db(merchant)


@merchant_url.route('', methods=["GET"])
def get_all():
    query = dict(request.args)
    query["fields"] = [v for v in query["fields"].split(',') if v] or []
    query["projection"] = {key: True for key in query["fields"]}
    merchant = merchant_table.find(
        {}, skip=query["skip"], limit=query["limit"], projection=query["projection"] or None)

    if not merchant:
        return {"code": 404, "message": "Merchant not found!"}, 404
    return get_str_from_id(list(merchant))


@merchant_url.route('/<id>', methods=["DELETE"])
def delete(id: int):
    if not id or not ObjectId().is_valid(id):
        return {"code": 400, "message": "invalid ID"}, 400

    merchant = merchant_table.delete({"filter": {"_id": ObjectId(id)}})

    if not merchant:
        return {"code": 404, "message": "Merchant not found!"}, 404

    return {"code": 200, "data": {"id": id}}
