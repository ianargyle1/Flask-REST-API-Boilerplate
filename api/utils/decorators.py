from flask import request, jsonify
from functools import wraps
from marshmallow.exceptions import ValidationError
from flask_jwt_extended import jwt_required, get_jwt_identity
from api.models.user import User


def validate_with(schema):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                kwargs['data'] = schema.load(request.json)
            except ValidationError as e:
                return {'errors': e.messages}, 400
            return f(*args, **kwargs)

        return decorated_function

    return decorator


def login_required(f):
    @wraps(f)
    @jwt_required
    def decorated_function(*args, **kwargs):
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        if current_user is None:
            return jsonify({'msg': 'Not authorized'}), 401
        kwargs['current_user'] = current_user
        return f(*args, **kwargs)
    return decorated_function
