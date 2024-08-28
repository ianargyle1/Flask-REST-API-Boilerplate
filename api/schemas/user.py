from marshmallow import Schema, fields, validate
from api import ma
from api.models.user import User


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        exclude = ['password_hash', 'created_at', 'updated_at']
