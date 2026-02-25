from functools import wraps

import jwt
from flask import request, jsonify

from app.models import User
from app.auth.helpers import decode_jwt_token


def token_required(f):
    """
    Decorator for checking token in the header and returning early if a token was not found or it's expired.
    If a valid token AND a user was found, add the user to the request object to be used in the views.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            token = token.split(" ")[1]
        except:
            return jsonify({'message': 'Token formatted incorrectly!'}), 401

        try:
            data = decode_jwt_token(token)
            current_user = User.query.filter_by(id=data['id']).first()
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Token is invalid!'}), 401

        if not current_user:
            return jsonify({'message': 'Token is invalid!'}), 401
        request.user = current_user

        return f(*args, **kwargs)

    return decorated
