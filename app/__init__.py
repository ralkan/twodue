from flask import Flask
from app.todos.views import bp as todos_bp


def create_app(env):
    app = Flask(__name__)
    app.register_blueprint(todos_bp, url_prefix="/todos")

    return app
