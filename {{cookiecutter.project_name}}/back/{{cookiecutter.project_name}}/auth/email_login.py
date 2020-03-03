import hashlib
from datetime import datetime

from flask import Blueprint, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity
from itsdangerous import URLSafeTimedSerializer
from peewee import DoesNotExist

from {{cookiecutter.project_name}}.core import config, db, cache, queue, mail
from {{cookiecutter.project_name}}.exceptions import *
from {{cookiecutter.project_name}}.models.social import User
from .utils import authenticated


def create_email_auth(app):
    jwt = JWTManager(app)
    email_auth_bp = Blueprint('email_login', __name__)

    @jwt.token_in_blacklist_loader
    def check_if_token_is_revoked(decrypted_token):
        user_id = decrypted_token['identity']['id']
        entry = cache.get('user_{}_valid'.format(user_id))
        if entry is None:
            return False
        return entry == 'false'

    @email_auth_bp.errorhandler(UserError)
    def handle_invalid_usage(error):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response

    @email_auth_bp.errorhandler(PasswordError)
    def handle_invalid_usage(error):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response

    @email_auth_bp.route('/login', methods=['POST'])
    @db.connection_context()
    def login():
        email = request.json.get('email')
        password = request.json.get('password')

        try:
            user = User.get(email=email)
        except DoesNotExist:
            raise UserNotFound

        if password is None:
            raise PasswordRequired
        password = hashlib.sha3_256('{}-{}'.format(config['email_auth']['hash_key'], password).encode())
        if user.password != password.hexdigest():
            raise EmailPasswordMismatch

        user.last_login = datetime.now()
        user.first_login = False
        user.save()
        access_token = create_access_token(identity=user.get_identity())

        return jsonify(access_token=access_token), 200

    @email_auth_bp.route('/sign-up', methods=['POST'])
    @db.connection_context()
    def sign_up():
        email = request.json.get('email')
        password = request.json.get('password')
        first_name = request.json.get('first_name')
        last_name = request.json.get('last_name')

        try:
            User.get(email=email)
            raise EmailAddressAlreadyTaken
        except DoesNotExist:
            if password is None:
                raise PasswordRequired
            if len(password) < 8:
                raise PasswordTooShort
            if email is None:
                raise EmailRequired
            if first_name is None:
                raise FirstNameRequired
            if last_name is None:
                raise LastNameRequired

            password = hashlib.sha3_256('{}-{}'.format(config['email_auth']['hash_key'], password).encode())

            user = User.create(email=email, password=password.hexdigest(), last_login=datetime.now(),
                               first_login=True, created_at=datetime.now(), first_name=first_name, last_name=last_name)

            activation_token = generate_activation_token(email)
            queue.enqueue(send_activation_email, user.email, activation_token)

            access_token = create_access_token(identity=user.get_identity())

            return jsonify(access_token=access_token), 200

    @email_auth_bp.route('/check-activation-token/<activation_token>')
    @db.connection_context()
    def get_email_from_activation_token(activation_token):
        email = check_activation_token(activation_token)
        try:
            user = User.get(email=email)
        except DoesNotExist:
            raise UserNotFound

        if user.account_activated:
            raise InvalidLink

        return jsonify(email=email)

    @email_auth_bp.route('/confirm-email/<activation_token>', methods=['POST'])
    @db.connection_context()
    @authenticated
    def confirm_email(activation_token):
        email = check_activation_token(activation_token)
        original_email = get_jwt_identity()['email']
        if original_email != email:
            raise InvalidLink

        try:
            user = User.get(email=email)
        except DoesNotExist:
            raise UserNotFound

        if user.account_activated:
            raise InvalidLink
        else:
            user.account_activated = True
            user.save()

            return 'Your account has been activated successfully!', 200

    @email_auth_bp.route('/resend-email', methods=['POST'])
    @db.connection_context()
    @authenticated
    def resend_email():
        email = get_jwt_identity()['email']

        try:
            user = User.get(email=email)
        except DoesNotExist:
            raise UserNotFound

        if user.account_activated:
            raise AccountAlreadyActivated

        activation_token = generate_activation_token(email)
        queue.enqueue(send_activation_email, email, activation_token)

        return 'A new email has been sent to {}'.format(email), 200

    @email_auth_bp.route('/forgot-password', methods=['POST'])
    @db.connection_context()
    def send_reset_link():
        email = request.json.get('email')

        if email is None:
            raise EmailRequired

        reset_token = generate_reset_token(email)
        queue.enqueue(send_reset_email, email, reset_token)

        return 'Instructions to reset your password have been sent to {}'.format(email), 200

    @email_auth_bp.route('/check-reset-token/<reset_token>')
    @db.connection_context()
    def get_email_from_reset_token(reset_token):
        email = check_reset_token(reset_token)
        try:
            user = User.get(email=email)
        except DoesNotExist:
            raise UserNotFound

        return jsonify(email=user.email)

    @email_auth_bp.route('/reset-password/<reset_token>', methods=['POST'])
    @db.connection_context()
    def reset_password(reset_token):
        email = check_reset_token(reset_token)
        password = request.json.get('password')

        if password is None:
            raise PasswordRequired
        if len(password) < 8:
            raise PasswordTooShort

        try:
            user = User.get(email=email)
        except DoesNotExist:
            raise UserNotFound

        password = hashlib.sha3_256('{}-{}'.format(config['email_auth']['hash_key'], password).encode())
        if user.password == password.hexdigest():
            raise SamePasswords
        else:
            user.password = password.hexdigest()
            user.save()

            return 'Your password has been reset successfully, log in with your new password', 200

    app.register_blueprint(email_auth_bp, url_prefix="/auth/email")


def generate_activation_token(email):
    serializer = URLSafeTimedSerializer(config['email_auth']['activation_key'])
    return serializer.dumps(email, salt=config['email_auth']['activation_password'])


def send_activation_email(to, token):
    mail.no_reply.connect()
    mail.no_reply.sendmail(to, 'Confirm your email address', 'confirm_email',
                           confirmation_url='{}/login/{}'.format(config['front_root_url'], token))
    mail.no_reply.close()


def check_activation_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(config['email_auth']['activation_key'])
    try:
        email = serializer.loads(
            token,
            salt=config['email_auth']['activation_password'],
            max_age=expiration
        )
    except:
        raise InvalidLink

    return email


def generate_reset_token(email):
    serializer = URLSafeTimedSerializer(config['email_auth']['reset_key'])
    return serializer.dumps(email, salt=config['email_auth']['reset_password'])


def send_reset_email(to, token):
    mail.no_reply.connect()
    mail.no_reply.sendmail(to, 'Instructions to reset your password', 'reset_password',
                           reset_url='{}/auth/email/reset-password/{}'.format(config['front_root_url'], token))
    mail.no_reply.close()


def check_reset_token(token, expiration=300):
    serializer = URLSafeTimedSerializer(config['email_auth']['reset_key'])
    try:
        email = serializer.loads(
            token,
            salt=config['email_auth']['reset_password'],
            max_age=expiration
        )
    except:
        raise InvalidLink

    return email
