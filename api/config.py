"""This module provides the application configurations"""
from os import urandom, path, getenv

BASEDIR = path.abspath(path.dirname(__name__))
SQLITE_DB = "sqlite:///" + path.join(BASEDIR, "db.sqlite")


class Config():
    """Main application configurations"""
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_TOKEN_LOCATION = 'headers'
    JWT_COOKIE_CSRF_PROTECT = True
    JWT_SECRET_KEY = urandom(32)
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']
    CELERY_TIMEZONE = getenv("CELERY_TIMEZONE", "UTC")
    BROKER_URL = getenv("BROKER_URL", "redis://localhost:6379/0")
    CELERY_RESULT_BACKEND = getenv(
        "CELERY_RESULT_BACKEND", "redis://localhost:6379/0"
    )
    CELERY_SEND_SENT_EVENT = True
    ADMIN_TOKEN = 'supersecretadmin'


class ProductionConfig(Config):
    """production application configurations"""
    pass


class DevelopmentConfig(Config):
    """development application configurations"""
    DEBUG = True
    JWT_COOKIE_CSRF_PROTECT = False
    SQLALCHEMY_DATABASE_URL = 'sqlite:///db.sqlite3'
    JWT_SECRET_KEY = 'topsecrettoken'
    SQLALCHEMY_DATABASE_URI = getenv("DATABASE_URL", SQLITE_DB)


class TestingConfig(Config):
    """testing application configurations"""
    TESTING = True


available_configs = dict(development=DevelopmentConfig,
                         production=ProductionConfig)
selected_config = getenv("FLASK_ENV", "development")
config = available_configs.get(selected_config, "development")
