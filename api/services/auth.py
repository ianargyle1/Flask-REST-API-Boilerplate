from api.models.user import User, AppleUser
from api.schemas.error import ErrorSchema
from api.schemas.auth import AuthResponseSchema
from api import db
from sqlalchemy.exc import IntegrityError
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity
from api.utils.apple_login import validate_apple_jwt


def register(first_name, last_name, email, password):
    # Create a new User instance
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


def login_with_apple(first_name, last_name, email, apple_id, token):
    if apple_id and token:
        is_valid, decoded_token = validate_apple_jwt(token)
        if not is_valid or decoded_token['sub'] != apple_id:
            return ErrorSchema(message='Invalid Apple token'), 400
        apple_user = AppleUser.query.filter_by(apple_id=apple_id).first()
        if apple_user:
            access_token = create_access_token(identity=apple_user.user_id)
            refresh_token = create_refresh_token(identity=apple_user.user_id)
            return AuthResponseSchema(token=access_token, refresh_token=refresh_token).to_dict(), 200
        elif first_name and last_name and email:
            new_user = User(first_name=first_name, last_name=last_name, email=email)
            new_apple_user = AppleUser(apple_id=apple_id, user=new_user)
            try:
                db.session.add(new_user)
                db.session.add(new_apple_user)
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
                return ErrorSchema(message='A user with this email already exists, please sign in with your password '
                                           'instead.').to_dict(), 400
            access_token = create_access_token(identity=new_user.id)
            refresh_token = create_refresh_token(identity=new_user.id)
            return AuthResponseSchema(token=access_token, refresh_token=refresh_token).to_dict(), 201
        else:
            return ErrorSchema(message='Missing required fields: first_name, last_name, email').to_dict(), 400
    else:
        return ErrorSchema(message='Missing required fields: apple_id, token').to_dict(), 400
