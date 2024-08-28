from flask import Blueprint
from api.utils.decorators import validate_with, login_required
from api.schemas.user import UserSchema
from api.services.user import retrieve, update

user = Blueprint('user', __name__, url_prefix='/user')


@user.get('/')
@login_required()
def retrieve_user(current_user):
    return retrieve(current_user)


@user.patch('/')
@login_required()
@validate_with(UserSchema(exclude=['id']))
def update_user(current_user, data):
    return update(current_user, data)
