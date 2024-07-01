from marshmallow import Schema, fields, validate
from api import ma
from api.models.user import User


class UserRegistrationSchema(Schema):
    first_name = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    last_name = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    email = fields.Email(required=True, validate=[validate.Email(), validate.Length(max=255)])
    password = fields.Str(required=True, validate=validate.Length(min=8, max=128))


class UserLoginSchema(Schema):
    email = fields.Email(required=True, validate=[validate.Email(), validate.Length(max=255)])
    password = fields.Str(required=True, validate=validate.Length(min=1, max=128))


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        exclude = ['password_hash', 'created_at', 'updated_at']
