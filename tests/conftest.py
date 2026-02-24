import pytest

from app import create_app, db
from app.models import Todo


@pytest.fixture()
def app():
    app = create_app('testing')

    with app.app_context():
        db.create_all()

    yield app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def todos(app):
    with app.app_context():
        todo1 = Todo(content="Milk")
        todo2 = Todo(content="Cheese")
        todo3 = Todo(content="Coffee")
        db.session.add(todo1)
        db.session.add(todo2)
        db.session.add(todo3)
        db.session.commit()
