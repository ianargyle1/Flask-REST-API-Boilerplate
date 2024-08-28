from flask import Blueprint
from api.schemas.auth import RegistrationSchema, LoginSchema
from api.utils.decorators import validate_with
from flask_jwt_extended import jwt_required
from api.services.auth import register, login, refresh

auth = Blueprint('auth', __name__, url_prefix='/auth')


@auth.post('/register')
@validate_with(RegistrationSchema())
def register_user(data):
    return register(**data)


@auth.post('/login')
@validate_with(LoginSchema())
def login_user(data):
    return login(**data)


@auth.post('/refresh')
@jwt_required(refresh=True)
def refresh_token():
    return refresh()