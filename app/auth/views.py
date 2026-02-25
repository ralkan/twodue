from flask import abort
from flask_smorest import Blueprint
from werkzeug.security import generate_password_hash, check_password_hash

bp = Blueprint('auth', __name__, url_prefix="/auth", description="Auth API")

from app import db
from app.models import User
from app.auth.helpers import create_jwt_token
from app.auth.schemas import RegisterRequestSchema, UserSchema, LoginRequestSchema


@bp.route("/register", methods=["POST"])
@bp.arguments(RegisterRequestSchema)
@bp.response(status_code=201, schema=UserSchema)
def register(user_schema):
    name = user_schema['name']
    email = user_schema['email']
    password = user_schema['password']

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        abort(400, "User already exists")

    hashed_password = generate_password_hash(password)
    user = User(name=name, email=email, password=hashed_password)

    db.session.add(user)
    db.session.commit()

    return user


@bp.route("/login", methods=["POST"])
@bp.arguments(LoginRequestSchema)
@bp.response(status_code=201, schema=UserSchema)
def login(user_schema):
    email = user_schema['email']
    password = user_schema['password']

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        return {'message': 'Invalid email or password'}, 401

    token = create_jwt_token(user)

    return {**UserSchema().dump(user), 'token': token}
