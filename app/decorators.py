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
        # Get the token from the Authorization header
        token = request.headers.get('Authorization')

        # Token was not found
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            # Split the token from "Bearer <token>" on the space
            token = token.split(" ")[1]
        except:
            return jsonify({'message': 'Token formatted incorrectly!'}), 401

        try:
            # Use the decode_jwt_token helper function to decode it and get the user ID out of the token
            data = decode_jwt_token(token)
            current_user = User.query.filter_by(id=data['id']).first()
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Token is invalid!'}), 401

        # No user was found with this user_id but the token was valid. Could this be faul play?
        if not current_user:
            # We should log this issue and possibly send an email to the administrator(s)
            return jsonify({'message': 'Token is invalid!'}), 401

        # Add the found user to the current request context for later use in the views
        request.user = current_user

        return f(*args, **kwargs)

    return decorated
