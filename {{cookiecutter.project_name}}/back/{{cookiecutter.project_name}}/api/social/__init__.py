from {{cookiecutter.project_name}}.api import api_bp, api

from .me import me
from .users import User, Users, ProfilePicture

api_bp.add_url_rule('/me', 'me', me)
api.add_resource(Users, '/users')
api.add_resource(User, '/users/<user_id>')
api.add_resource(ProfilePicture, '/users/<user_id>/profile-picture')
