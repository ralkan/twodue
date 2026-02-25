from flask import Flask
from flask_smorest import Api
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

from config import config

db = SQLAlchemy()
ma = Marshmallow()
api = Api()

from app.utils import AzureKeyVaultClient
from app.auth.views import bp as auth_bp
from app.todos.views import bp as todos_bp

def create_app(env):
    app = Flask(__name__)
    conf = config[env]

    # Only get SECRET_KEY from Azure if env is not "testing"
    # For pytest we don't need to use the Azure Key Vault
    if conf.USE_AZURE_SECRET:
        kv_client = AzureKeyVaultClient(conf)
        conf.SECRET_KEY = kv_client.get_secret(conf.SECRET_NAME).value

    app.config.from_object(conf)

    db.init_app(app)
    ma.init_app(app)
    api.init_app(app)

    api.register_blueprint(auth_bp)
    api.register_blueprint(todos_bp)

    return app
