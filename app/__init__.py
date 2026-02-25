from flask import Flask
from flask_smorest import Api
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

from config import config

db = SQLAlchemy()
ma = Marshmallow()
api = Api()

from app.auth.views import bp as auth_bp
from app.todos.views import bp as todos_bp

def create_app(env):
    app = Flask(__name__)
    app.config.from_object(config[env])

    db.init_app(app)
    ma.init_app(app)
    api.init_app(app)

    api.register_blueprint(auth_bp)
    api.register_blueprint(todos_bp)

    return app
