"""This is the main application"""
# Package imports
from flask import Flask

# Local module imports
from api.extensions import register_extensions
from api.controller import register_routes
from api.config import config


def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
    app.url_map.strict_slashes = False
    register_extensions(app)
    register_routes(app)
    return app


def create_worker_app():
    """Minimal App without routes for celery worker."""
    app = Flask(__name__)
    app.config.from_object(config)
    register_extensions(app, worker=True)
    return app
