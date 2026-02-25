import pytest

from flask.testing import FlaskClient
from werkzeug.security import generate_password_hash

from app import create_app, db
from app.models import Todo, User


USER_EMAIL = "me@test.com"
USER_PASS = "abc123"


class AuthFlaskClient(FlaskClient):
    """
    Custom Auth test client class that retrieves a token
    and automatically adds it to the header for each request.
    """
    _token = None

    def open(self, *args, **kwargs):
        if 'login' not in args[0] and self._token is None:
            self.get_token()
        kwargs.setdefault('headers', {'Authorization': f'Bearer {self._token}'})
        return super().open(*args, **kwargs)

    def get_token(self):
        response = self.post('/auth/login', json={"email": USER_EMAIL, "password": USER_PASS})
        self._token = response.json['token']


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
def auth_client(app, user):
    app.test_client_class = AuthFlaskClient
    test_client = app.test_client()
    return test_client


@pytest.fixture()
def user(app):
    with app.app_context():
        hashed_password = generate_password_hash(USER_PASS)
        user = User(email=USER_EMAIL, name="Test User 1", password=hashed_password)
        db.session.add(user)
        db.session.commit()
    return user


@pytest.fixture()
def otheruser(app):
    with app.app_context():
        hashed_password = generate_password_hash(USER_PASS)
        user = User(email="temp@user.com", name="Test User 2", password=hashed_password)
        db.session.add(user)
        db.session.commit()
    return user


@pytest.fixture()
def todos(app, user, otheruser):
    with app.app_context():
        todo1 = Todo(content="Milk", user=user)
        todo2 = Todo(content="Cheese", user=user)
        todo3 = Todo(content="Coffee", user=user)

        # TODO: Add tests for user todos to see if users only see their own todos
        todo4 = Todo(content="Goat Cheese", user=otheruser)
        db.session.add(todo1)
        db.session.add(todo2)
        db.session.add(todo3)
        db.session.add(todo4)
        db.session.commit()
