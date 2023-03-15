from datetime import datetime

from marshmallow import Schema, fields

from src.models import common_fields


# class RuleSchema(Schema):
#     _id = fields.Str()
#     name = fields.Str(required=True)
#     created_by = fields.Str()
#     updated_by = fields.Str()
#     created_at = fields.DateTime(default=datetime.datetime.utcnow())
#     updated_at = fields.DateTime(default=datetime.datetime.utcnow())


class RuleSchema(Schema):
    name = fields.Str(required=True)
    status = fields.Boolean(default=True)

    class Meta:
        fields = ['name', 'status'] + common_fields
