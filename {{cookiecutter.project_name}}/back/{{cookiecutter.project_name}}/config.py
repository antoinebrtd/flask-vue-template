from datetime import timedelta

from .core import config
from .core.utils import DateTimeEncoder


class FlaskConfig(object):
    ENV = config['flask'].get('env', 'production')
    DEBUG = config['flask'].get('debug', False)

    SECRET_KEY = config['flask'].get('oauth_secret', False)

    JWT_SECRET_KEY = config['flask'].get('jwt_secret', False)
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(seconds=config['flask'].get('jwt_expiration', 900))
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']

    RESTFUL_JSON = {'separators': (', ', ': '),
                    'indent': 2,
                    'cls': DateTimeEncoder}


flask_config = FlaskConfig
