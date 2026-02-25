# TwoDue

Your go-to ToDo application to do your due too!

A REST API built with Flask for managing todos with user authentication, pagination, sorting, and search.

## Tech Stack

- **Flask** — Web framework
- **Flask-Smorest** — REST API with OpenAPI/Swagger documentation
- **Flask-SQLAlchemy** — ORM
- **Flask-Migrate** — Database migrations (Alembic)
- **Marshmallow** — Request/response serialization and validation
- **PyJWT** — JSON Web Token authentication
- **SQLite** — Database
- **Gunicorn** — Production WSGI server

## Project Structure

```
twodue/
├── app/
│   ├── __init__.py          # App factory
│   ├── models.py            # User and Todo models
│   ├── decorators.py        # JWT token_required decorator
│   ├── helpers.py           # Pagination helper
│   ├── auth/
│   │   ├── views.py         # Register and login endpoints
│   │   ├── schemas.py       # Auth request/response schemas
│   │   └── helpers.py       # JWT token creation and decoding
│   └── todos/
│       ├── views.py         # Todo CRUD endpoints
│       ├── schemas.py       # Todo request/response schemas
│       ├── filters.py       # Query parameter filters and enums
│       └── mixins.py        # User visibility mixin
├── tests/
│   ├── conftest.py          # Pytest fixtures
│   └── test_todos.py        # Todo endpoint tests
├── migrations/              # Alembic migration files
├── config.py                # Configuration classes
├── wsgi.py                  # WSGI entry point
├── requirements.txt
└── .env
```

## Setup

### Prerequisites

- Python 3.10+

### Installation

```bash
# Clone the repository
git clone https://github.com/ralkan/twodue.git
cd twodue

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Environment Variables

Create a `.env` file in the project root:

```
ENVIRONMENT=development
DEFAULT_PAGINATION_COUNT=2
SECRET_KEY="your-secret-key"
```

| Variable | Description | Default |
|---|---|---|
| `ENVIRONMENT` | App environment (`development` or `testing`) | `development` |
| `DEFAULT_PAGINATION_COUNT` | Items per page | `2` |
| `SECRET_KEY` | Secret key for JWT token signing | — |

### Database Setup

```bash
flask db upgrade
```

## Running the App

### Development

```bash
flask run --port 8000 --debug
```

### Production

```bash
gunicorn -w 1 wsgi:app
```

### API Documentation

Once the app is running, Swagger UI is available at `/docs`.

## API Endpoints

### Authentication

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/auth/register` | Register a new user |
| `POST` | `/auth/login` | Login and receive a JWT token |

### Todos (all require authentication)

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/todos/` | List todos |
| `POST` | `/todos/` | Create a todo |
| `GET` | `/todos/<id>` | Get a single todo |
| `PUT` | `/todos/<id>` | Update a todo |
| `DELETE` | `/todos/<id>` | Delete a todo |

#### Query Parameters for `GET /todos/`

| Parameter | Type | Default | Description |
|---|---|---|---|
| `page` | integer | `1` | Page number |
| `search` | string | — | Filter by content prefix |
| `order_by` | string | `id` | Sort field (`id`, `content`, `done`) |
| `order` | string | `asc` | Sort direction (`asc`, `desc`) |

## Authentication

All todo endpoints require a JWT token in the `Authorization` header:

```
Authorization: Bearer <token>
```

### Usage Flow

1. **Register** a user:
   ```bash
   curl -X POST http://localhost:8000/auth/register \
     -H "Content-Type: application/json" \
     -d '{"name": "John", "email": "john@example.com", "password": "secret"}'
   ```

2. **Login** to get a token:
   ```bash
   curl -X POST http://localhost:8000/auth/login \
     -H "Content-Type: application/json" \
     -d '{"email": "john@example.com", "password": "secret"}'
   ```

3. **Use the token** in subsequent requests:
   ```bash
   curl http://localhost:8000/todos/ \
     -H "Authorization: Bearer <token>"
   ```

Tokens expire after 1 hour.

## Testing

Tests use an in-memory SQLite database and run independently of the development database.

```bash
python -m pytest
```

With verbose output:

```bash
python -m pytest -v
```
