from datetime import datetime

from marshmallow import Schema, fields
from configs.configs import CONFIG_ACCOUNT_DB as db

from src.models.schemas import common_fields


class MerchantSchema(Schema):
    name = fields.Str(required=True)

    class Meta:
        fields = ['name', 'updated_by'] + common_fields
