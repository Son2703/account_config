import datetime

from marshmallow import Schema, fields

from src.models.schemas import common_fields


class UserBaseSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)


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
    user_ids = fields.List(required=True, cls_or_instance=fields.Str())

    class Meta:
        fields = ['user_ids']


# class InsertByFileSchema(Schema):
#     list = fields(required=True, tuple_fields=fields.Dict())

#     class Meta:
#         # fields = ['list']
#         tuple_fields = ['list']

class BulkInsertSchema(Schema):
    array = fields.List(required=True, cls_or_instance=fields.Dict())

    class Meta:
        fields = ['list']

