import datetime

from marshmallow import Schema, fields

from src.models import common_fields


class UserBaseSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)

# class UserSchema(UserBaseSchema):
#     _id = fields.Str()
#     id_merchant = fields.Str(required=True)
#     last_login = fields.DateTime(default=datetime.datetime.utcnow())
#     login_fail_number = fields.Number(default=0)
#     status = fields.Boolean(default=True)
#     created_by = fields.Str()
#     updated_by = fields.Str()
#     created_at = fields.DateTime(default=datetime.datetime.utcnow())
#     updated_at = fields.DateTime(default=datetime.datetime.utcnow())


class ChangePasswordSchema(UserBaseSchema):
    new_password = fields.Str(required=True)
    password_confirm = fields.Str(required=True)

    class Meta:
        fields = ['username', 'password', 'new_password', 'password_confirm'] + common_fields


class SignInSchema(UserBaseSchema):
    id_merchant = fields.Str(required=True)

    class Meta:
        fields = ['username', 'password', 'id_merchant']


class UnlockUserSchema(Schema):
    user_ids = fields.List(required=True)

    class Meta:
        fields = ['user_ids']


class InsertByFileSchema(Schema):
    list = fields.Tuple(required=True)

    class Meta:
        fields = ['list']


class BulkInsertSchema(Schema):
    array = fields.List(required=True)

    class Meta:
        fields = ['list']

