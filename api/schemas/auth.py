from marshmallow import Schema, fields, validate


class RegistrationSchema(Schema):
    first_name = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    last_name = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    email = fields.Email(required=True, validate=[validate.Email(), validate.Length(max=255)])
    password = fields.Str(required=True, validate=validate.Length(min=8, max=128))


class LoginSchema(Schema):
    email = fields.Email(required=True, validate=[validate.Email(), validate.Length(max=255)])
    password = fields.Str(required=True, validate=validate.Length(min=1, max=128))


class LoginWithAppleSchema(Schema):
    first_name = fields.Str(required=False, validate=validate.Length(min=1, max=50))
    last_name = fields.Str(required=False, validate=validate.Length(min=1, max=50))
    email = fields.Email(required=True, validate=[validate.Email(), validate.Length(max=255)])
    apple_id = fields.Str(required=True, validate=validate.Length(min=1))
    token = fields.Str(required=True, validate=validate.Length(min=1))


class AuthResponseSchema(Schema):
    token = fields.Str(required=False)
    refresh_token = fields.Str(required=False)

    def __init__(self, token=None, refresh_token=None, **kwargs):
        super().__init__(**kwargs)
        self.token = token
        self.refresh_token = refresh_token

    def to_dict(self):
        return self.dump(self)
