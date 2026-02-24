import os
from flask_migrate import Migrate
from app import create_app, db, models

app = create_app(os.getenv('ENVIRONMENT'))
migrate = Migrate(app, db)
