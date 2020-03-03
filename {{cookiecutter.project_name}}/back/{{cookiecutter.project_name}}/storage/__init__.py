from botocore.exceptions import ClientError
import flask
from flask import Blueprint, request

from {{cookiecutter.project_name}}.core import storage, config


def create_storage_gw(app):
    storage_bp = Blueprint('storage-gw', __name__)

    @storage_bp.route('/download')
    def download():
        filepath = request.args.get('filepath')
        try:
            object = storage.get_object(Bucket=config['storage']['bucket'], Key=filepath)['Body']
        except ClientError:
            return '', 404

        response = flask.make_response(object.read())
        response.headers['content-type'] = 'application/octet-stream'
        return response

    app.register_blueprint(storage_bp, url_prefix="/storage")
