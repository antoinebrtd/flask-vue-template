import random
import string
from datetime import datetime

import requests
from flask import Blueprint, jsonify, request, redirect
from flask_jwt_extended import JWTManager, create_access_token
from itsdangerous import URLSafeTimedSerializer, SignatureExpired

from {{cookiecutter.project_name}}.core import cache, config, db, facebook_config
from {{cookiecutter.project_name}}.exceptions.users import *
from {{cookiecutter.project_name}}.models.social import User

TOKEN_URL = 'https://graph.facebook.com/debug_token?input_token={}&access_token={}'
ME_URL = 'https://graph.facebook.com/me?fields=first_name,last_name,email&access_token={}'
PICTURE_URL = 'https://graph.facebook.com/{}/picture'
SCOPES = 'public_profile,email,birthday'


def create_facebook_auth(app):
    jwt = JWTManager(app)
    facebook_auth_bp = Blueprint('facebook_login', __name__)

    def credentials_to_dict(credentials):
        return {'token': credentials['access_token'],
                'fb_user_id': credentials['user_id'],
                'expires_in': credentials['expires_in'],
                'issued_at': credentials['issued_at'],
                'scopes': credentials['scopes']}

    @facebook_auth_bp.errorhandler(UserError)
    def handle_invalid_usage(error):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response

    @facebook_auth_bp.route('/callback')
    def callback():
        code = request.args.get('code')
        state = request.args.get('state')
        if code is None:
            return redirect('{}?error=access_denied'.format(config['oauth']['facebook']['front_callback']))
        if not check_state(state):
            return redirect('{}?error=invalid_link'.format(config['oauth']['facebook']['front_callback']))
        return redirect('{}?code={}'.format(config['oauth']['facebook']['front_callback'], code))

    @facebook_auth_bp.route('/login')
    def login():
        state = generate_state()
        authorization_url = '{}?client_id={}&redirect_uri={}&state={}'.format(
            facebook_config['auth_uri'],
            facebook_config['app_id'],
            config['oauth']['facebook']['callback'],
            state
        )
        return jsonify({'url': authorization_url})

    @facebook_auth_bp.route('/authorize')
    @db.connection_context()
    def authorize():
        code = request.args.get('code')
        params = {'client_id': facebook_config['app_id'], 'redirect_uri': config['oauth']['facebook']['callback'],
                  'client_secret': facebook_config['client_secret'], 'code': code}
        credentials = requests.get(facebook_config['token_uri'], params=params).json()
        token_inspection = requests.get(
            TOKEN_URL.format(credentials['access_token'], facebook_config['app_token'])).json()

        credentials.update(token_inspection['data'])

        profile = requests.get(ME_URL.format(credentials['access_token']))

        user_info = profile.json()
        email = user_info.get('email')
        user, created = User.get_or_create(email=email, defaults={
            'first_name': user_info.get('first_name'),
            'last_name': user_info.get('last_name'),
            'picture': PICTURE_URL.format(credentials['user_id']),
            'last_login': datetime.now(),
            'created_at': datetime.now(),
            'first_login': True,
            'account_activated': True
        })
        if not created:
            if not user.account_activated:
                raise EmailNotConfirmed
            if not user.picture:
                user.picture = user_info.get('picture')
            user.last_login = datetime.now()
            user.first_login = False
            user.save()

        user.add_facebook_credentials(credentials_to_dict(credentials))

        access_token = create_access_token(identity=user.get_identity())

        return jsonify(access_token=access_token), 200

    @jwt.token_in_blacklist_loader
    def check_if_token_is_revoked(decrypted_token):
        user_id = decrypted_token['identity']['id']
        entry = cache.get('user_{}_valid'.format(user_id))
        if entry is None:
            return False
        return entry == 'false'

    app.register_blueprint(facebook_auth_bp, url_prefix="/auth/facebook")


def generate_state():
    letters = string.ascii_lowercase
    random_string = ''.join(random.choice(letters) for i in range(30))
    serializer = URLSafeTimedSerializer(config['oauth']['facebook']['state_key'])
    return serializer.dumps(random_string)


def check_state(state, expiration=300):
    if state is None:
        return False

    serializer = URLSafeTimedSerializer(config['oauth']['facebook']['state_key'])
    try:
        serializer.loads(state, max_age=expiration)
    except SignatureExpired:
        return False

    return True
