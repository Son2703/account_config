from flask import Blueprint

from src.models.merchant_schemas import MerchantSchema

test_print = Blueprint('page', __name__)

@test_print('test', methods=['GET'])
def test_sc():
    MerchantSchema().load({'name': {'a':1}})
    return 'acts'
