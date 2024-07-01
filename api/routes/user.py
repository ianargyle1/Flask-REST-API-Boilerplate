from flask import Blueprint, request
from api.schemas.user import UserRegistrationSchema, UserLoginSchema
from api.utils.decorators import validate_with, login_required
from flask_jwt_extended import jwt_required
from api.services.user import (
    register,
    login,
    refresh,
    retrieve,
    update_first_name,
    update_last_name,
    update_email
)

user = Blueprint('user', __name__, url_prefix='/user')


@user.post('/register')
@validate_with(UserRegistrationSchema())
def register_user(data):
    return register(**data)


@user.post('/login')
@validate_with(UserLoginSchema())
def login_user(data):
    return login(**data)


@user.post('/refresh')
@jwt_required(refresh=True)
def refresh_token():
    return refresh()


@user.get('/')
@login_required()
def retrieve_user(current_user):
    return retrieve(current_user)


@user.patch('/first_name')
@login_required()
@validate_with(UserRegistrationSchema(only=['first_name']))
def update_user_first_name(current_user, data):
    return update_first_name(current_user, data['first_name'])


@user.patch('/last_name')
@login_required()
@validate_with(UserRegistrationSchema(only=['last_name']))
def update_user_last_name(current_user, data):
    return update_last_name(current_user, data['last_name'])


@user.patch('/email')
@login_required()
@validate_with(UserRegistrationSchema(only=['email']))
def update_user_email(current_user, data):
    return update_email(current_user, data['email'])
