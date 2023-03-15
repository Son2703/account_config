from bson import ObjectId
from marshmallow import Schema, fields

Schema.TYPE_MAPPING[ObjectId] = fields.Str()

common_fields = ['created_at', 'updated_at', 'created_by', 'updated_by']
