from marshmallow import Schema, fields

from src.models.schemas import common_fields


class MerchantConfigSchenma(Schema):
    id_merchant = fields.String(require=False)
    val_name = fields.Dict(require=False)
    val_pass = fields.Dict(require=False)
    change_pass_moth = fields.Dict(require=False)
    unique_old_pass = fields.Dict(require=False)
    require_change_pass = fields.Dict(require=False)
    unique_pass = fields.Dict(require=False)
    lock_account = fields.Dict(require=False)

    class Meta:
        fields = ["id_merchant", 'val_name', 'val_pass', 'change_pass_moth', 'unique_old_pass', 'require_change_pass', 'unique_pass', 'lock_account'] + common_fields

class BaseValSchema(Schema):
    min_len = fields.Integer(require=True, min=0)
    max_len = fields.Integer(require=True, min=0)
    all = fields.Dict(require=True, 
                      )
    at_least = fields.Dict(require=True)

class ValNameSchema(BaseValSchema):
    pass

class ValPassSchema(BaseValSchema):
    upper = fields.Dict(require=True)
    lowecase = fields.Dict(require=True)

class BaseCheckSchema(Schema):
    check = fields.Boolean(require=True)

class BaseValueSchema(BaseCheckSchema):
    value = fields.Integer(require=True, min=0)

class LockAccountSchema(BaseValueSchema):
    time_lock = fields.Integer(require=False)
