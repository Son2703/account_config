from datetime import datetime

from marshmallow import Schema, fields

from src.models import common_fields


class MerchantSchema(Schema):
    name = fields.Str(required=True)

    class Meta:
        fields = ['name'] + common_fields
