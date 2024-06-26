from flask import jsonify
from api.models.user import User
from api.schemas.user import UserSchema
from api import db
from sqlalchemy.exc import IntegrityError
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity


def register(name, email, password):
    # Create a new User instance
    new_user = User(name=name, email=email)
    new_user.set_password(password)

    try:
        # Add the new user to the session and commit it
        db.session.add(new_user)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return {'error': 'A user with this email already exists.'}, 400

    access_token = create_access_token(identity=new_user.id)
    refresh_token = create_refresh_token(identity=new_user.id)
    return jsonify(access_token=access_token, refresh_token=refresh_token), 201


def login(email, password):
    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password_hash, password):
        return {'error': 'Invalid email or password'}, 400

    access_token = create_access_token(identity=user.id)
    refresh_token = create_refresh_token(identity=user.id)
    return jsonify(access_token=access_token, refresh_token=refresh_token), 200


def refresh():
    current_user_id = get_jwt_identity()
    access_token = create_access_token(identity=current_user_id)
    refresh_token = create_refresh_token(identity=current_user_id)
    return jsonify(access_token=access_token, refresh_token=refresh_token), 200


def retrieve(current_user):
    user_schema = UserSchema()
    return user_schema.dump(current_user), 200


def update_name(current_user, new_name):
    current_user.name = new_name
    db.session.commit()
    return {'message': 'User updated successfully'}, 200


def update_email(current_user, new_email):
    current_user.email = new_email
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return {'error': 'A user with this email already exists.'}, 400
    return {'message': 'User updated successfully'}, 200


def update_password(current_user, new_password):
    current_user.set_password(new_password)
    db.session.commit()
    return {'message': 'User updated successfully'}, 200
