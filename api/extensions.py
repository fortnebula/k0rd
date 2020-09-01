from celery import Celery
from api.database import init_db
from flask_jwt_extended import JWTManager
from api.models import users

celery = Celery()


def register_extensions(app, worker=False):
    jwt = JWTManager(app) # noqa

    @jwt.token_in_blacklist_loader
    def check_if_token_in_blacklist(decrypted_token):
        jti = decrypted_token['jti']
        query = users.Tokens.query.filter_by(api_key=jti).first()
        if query is None:
            return False
        elif query.revoked is False:
            return False
        elif query.revoked is True:
            return True

    init_db(app)
    # load celery config
    celery.config_from_object(app.config)

    if not worker:
        # register celery irrelevant extensions
        pass
