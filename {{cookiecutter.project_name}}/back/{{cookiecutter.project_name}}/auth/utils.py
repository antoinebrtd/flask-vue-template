from functools import wraps

from flask import request
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity

from {{cookiecutter.project_name}}.core import logger


def authenticated(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        me = get_jwt_identity()
        user = me.get('email')
        if user is None:
            user = me.get('id')
        logger.info('[Request] Path : {} {} | User : {}'.format(request.method, request.full_path, user))
        return fn(*args, **kwargs)

    return wrapper
