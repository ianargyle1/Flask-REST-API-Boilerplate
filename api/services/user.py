from api.schemas.error import ErrorSchema
from api.schemas.user import UserSchema
from api import db
from sqlalchemy.exc import IntegrityError


def retrieve(current_user):
    user_schema = UserSchema()
    return user_schema.dump(current_user), 200


def update(current_user, new_user):
    current_user.first_name = new_user.first_name
    current_user.last_name = new_user.last_name
    current_user.email = new_user.email
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return ErrorSchema(message='A user with this email already exists.'), 400
    user_schema = UserSchema()
    return user_schema.dump(current_user), 200
