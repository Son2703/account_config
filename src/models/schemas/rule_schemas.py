from datetime import datetime

from marshmallow import Schema, fields

from src.models.schemas import common_fields


class RuleSchema(Schema):
    name = fields.Str(required=True)
    status = fields.Boolean(default=True)

    class Meta:
        fields = ['name', 'status'] + common_fields
