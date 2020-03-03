import rq_dashboard
from flask import Flask
from flask_cors import CORS

from .api import register_api
from .auth import {%- if cookiecutter.google_login == 'y' %} create_google_auth{%- endif %}{%- if cookiecutter.email_login == 'y' %}, create_email_auth{%- endif %}{%- if cookiecutter.facebook_login == 'y' %}, create_facebook_auth{%- endif %}
from .config import flask_config
from .core.cache import REDIS_URL
{%- if cookiecutter.storage == 'y' %}from .storage import create_storage_gw{%- endif %}


def create_app(api=True):
    app = Flask(__name__)
    CORS(app, resources={r"*": {"origins": "*"}}, supports_credentials=True)
    app.config.from_object(flask_config)

    {%- if cookiecutter.email_login == 'y' %}
    create_email_auth(app)
    {%- endif %}
    {%- if cookiecutter.google_login == 'y' %}
    create_google_auth(app)
    {%- endif %}
    {%- if cookiecutter.facebook_login == 'y' %}
    create_facebook_auth(app)
    {%- endif %}
    {% - if cookiecutter.storage == 'y' %}
    create_storage_gw(app)
    {%- endif %}

    if api:
        register_api(app)

    app.config.from_object(rq_dashboard.default_settings)
    app.config['REDIS_URL'] = REDIS_URL
    app.register_blueprint(rq_dashboard.blueprint, url_prefix="/jobs")

    return app
