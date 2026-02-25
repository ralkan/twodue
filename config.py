import os
from dotenv import load_dotenv

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))


class Config:
    DEFAULT_PAGINATION_COUNT = int(os.environ.get("DEFAULT_PAGINATION_COUNT")) or 2
    API_TITLE = os.environ.get('API_TITLE') or 'TwoDue'
    API_VERSION = 'v1'
    OPENAPI_VERSION = '3.0.3'
    OPENAPI_URL_PREFIX = '/'
    OPENAPI_SWAGGER_UI_PATH = '/docs'
    OPENAPI_SWAGGER_UI_URL = 'https://cdn.jsdelivr.net/npm/swagger-ui-dist@3.25.0/'
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'uwsecnqimr2a&m&di7*t3u!wmei_4224jz1!aycts-1b3ksr_@'
    SSL_REDIRECT = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True

    # Azure specific config
    # Set to False for assessment. Don't use this since it requires some setup in Azure
    USE_AZURE_SECRET = False
    # USE_AZURE_SECRET = True
    KEY_VAULT_NAME = os.environ.get('KEY_VAULT_NAME') or "twodue-mi-kv"
    SECRET_NAME = os.environ.get('SECRET_NAME') or "SECRETKEY"
    KV_URI = f"https://{KEY_VAULT_NAME}.vault.azure.net/"


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3')


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite://'

    # Azure specific config
    # Disable Azure Key Vault for testing due to slowing down tests
    USE_AZURE_SECRET = False


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,

    'default': DevelopmentConfig
}
