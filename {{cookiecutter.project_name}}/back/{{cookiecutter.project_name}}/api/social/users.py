import werkzeug

from flask import request
from flask_jwt_extended import get_jwt_identity
from flask_restful import Resource, reqparse

from {{cookiecutter.project_name}}.auth import authenticated
from {{cookiecutter.project_name}}.managers.social import users


class Users(Resource):
    @authenticated
    def get(self):
        search = request.args.get('search')
        user_list = users.get_all(search=search)
        return {'msg': 'success', 'users': user_list}


class User(Resource):
    @authenticated
    def get(self, user_id):
        profile, account_activated, first_login = users.get(user_id).get_data()
        return {
            'msg': 'success',
            'user': {'profile': profile, 'account_activated': account_activated, 'first_login': first_login}
        }

    @authenticated
    def patch(self, user_id):
        field = request.args['field']
        info = request.json['value']
        identity = get_jwt_identity()
        profile, account_activated, first_login = users.update_personal_info(user_id, field, info)
        if identity['id'] != int(user_id):
            return {'msg': 'forbidden'}, 403

        return {
            'msg': 'success',
            'user': {'profile': profile, 'account_activated': account_activated, 'first_login': first_login}
        }

    @authenticated
    def delete(self, user_id):
        identity = get_jwt_identity()
        if identity['id'] != int(user_id):
            return {'msg': 'forbidden'}, 403
        users.delete_user(user_id)
        return {'msg': 'success'}


class ProfilePicture(Resource):
    @authenticated
    def patch(self, user_id):
        identity = get_jwt_identity()
        if identity['id'] != int(user_id):
            return {'error': 'You are not allowed to modify this profile picture'}, 403

        parser = reqparse.RequestParser()
        parser.add_argument('file', type=werkzeug.datastructures.FileStorage, location='files')
        data = parser.parse_args()
        profile_picture = data['file']

        if profile_picture.filename.split('.')[-1] not in ['jpeg', 'jpg', 'png', 'JPG', 'JPEG', 'PNG']:
            return {'error': 'You can only upload images in jpg or png format'}, 403

        user = users.update_profile_picture(user_id, profile_picture)

        return {'msg': 'success', 'user': user}
