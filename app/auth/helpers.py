from datetime import timezone, datetime, timedelta

import jwt
from flask import current_app


def create_jwt_token(user):
    return jwt.encode(
        {'id': user.id, 'exp': datetime.now(timezone.utc) + timedelta(hours=1)},
        current_app.config['SECRET_KEY'], algorithm="HS256")


def decode_jwt_token(token):
    return jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
