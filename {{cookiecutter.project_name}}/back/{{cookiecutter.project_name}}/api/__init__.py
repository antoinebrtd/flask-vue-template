import time

from flask import Blueprint, current_app, g, request
from flask_restful import Api

from {{cookiecutter.project_name}}.api.errors import register_errors
from {{cookiecutter.project_name}}.core import logger, db

api_bp = Blueprint('api', __name__)


class AdvancedApi(Api):
    def handle_error(self, e):
        for val in current_app.error_handler_spec.values():
            for handler in val.values():
                registered_error_handlers = list(filter(lambda x: isinstance(e, x), handler.keys()))
                if len(registered_error_handlers) > 0:
                    raise e
        return super().handle_error(e)


api = AdvancedApi(api_bp)


def register_api(app):
    @api_bp.before_request
    def before_request():
        g.start = time.time()
        db.connect(reuse_if_open=True)

    @api_bp.teardown_request
    def after_request(exception=None):
        db.close()
        diff = time.time() - g.start
        logger.info('[Request time] Path : {} {} | Time : {}s'.format(request.method, request.full_path, diff))

    import {{cookiecutter.project_name}}.api.jobs
    import {{cookiecutter.project_name}}.api.social
    import {{cookiecutter.project_name}}.api.utils

    register_errors(api_bp)

    app.register_blueprint(api_bp, url_prefix="/api/v1")

    logger.debug('Blueprints successfully registered.')
