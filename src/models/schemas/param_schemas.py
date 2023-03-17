from marshmallow import Schema, fields


class ParamSchema(Schema):
    id_merchant = fields.Str(required=True)


class ParamIdSchema(Schema):
    id = fields.Str(required=True)