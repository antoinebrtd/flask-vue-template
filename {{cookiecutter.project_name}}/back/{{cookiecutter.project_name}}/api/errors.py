from elasticsearch import NotFoundError
from flask import jsonify
from peewee import DoesNotExist

from {{cookiecutter.project_name}}.exceptions import APIError


def register_errors(api):
    @api.errorhandler(APIError)
    def handle_invalid_usage(error):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response

    @api.errorhandler(DoesNotExist)
    def handle_invalid_usage(error):
        resource = error.args[0].split('>')[0].split(' ')[1]
        response = jsonify({"msg": "{} not found".format(resource)})
        response.status_code = 404
        return response

    @api.errorhandler(NotFoundError)
    def handle_invalid_usage(error):
        response = jsonify({"msg": "{} {} not found".format(error.info['_index'].capitalize(), error.info['_id'])})
        response.status_code = 404
        return response
