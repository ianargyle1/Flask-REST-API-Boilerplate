from api.models.user import User
from api.schemas.error import ErrorSchema
from api.schemas.auth import AuthResponseSchema
from api import db
from sqlalchemy.exc import IntegrityError
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity


def register(first_name, last_name, email, password):
    # Create a new User instance5,xw/d=+|Z01
    new_user = User(first_name=first_name, last_name=last_name, email=email)
    new_user.set_password(password)

    try:
        # Add the new user to the session and commit it
        db.session.add(new_user)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return ErrorSchema(message='A user with this email already exists.').to_dict(), 400

    access_token = create_access_token(identity=new_user.id)
    refresh_token = create_refresh_token(identity=new_user.id)
    return AuthResponseSchema(token=access_token, refresh_token=refresh_token).to_dict(), 201


def login(email, password):
    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password_hash, password):
        return ErrorSchema(message='Invalid email or password'), 400

    access_token = create_access_token(identity=user.id)
    refresh_token = create_refresh_token(identity=user.id)
    return AuthResponseSchema(token=access_token, refresh_token=refresh_token).to_dict(), 200


def refresh():
    current_user_id = get_jwt_identity()
    access_token = create_access_token(identity=current_user_id)
    refresh_token = create_refresh_token(identity=current_user_id)
    return AuthResponseSchema(token=access_token, refresh_token=refresh_token).to_dict(), 200
