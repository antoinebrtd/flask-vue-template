import uuid

from peewee import DoesNotExist

from {{cookiecutter.project_name}}.core import cache, storage, config
from {{cookiecutter.project_name}}.exceptions import *
from {{cookiecutter.project_name}}.models.social.user import User


def get_all(search=None) -> list:
    users = []
    if search is None or search == '':
        query = User.select()
    else:
        query = User.select().where(
            (User.first_name.contains(search)) |
            (User.last_name.contains(search)))

    for user in query:
        profile, account_activated, first_login = user.get_data()
        users.append({'profile': profile, 'account_activated': account_activated, 'first_login': first_login})
    logger.debug('Get all users from db. Number of users : {}'.format(len(users)))

    return users


def get(user_id) -> User:
    try:
        user = User.get(User.id == user_id)
        return user
    except DoesNotExist:
        raise UserNotFound


def get_by_mail(mail) -> User:
    try:
        user = User.get(User.email == mail)
        return user
    except DoesNotExist:
        raise UserNotFound


def update_personal_info(user_id, field, info):
    user = get(user_id)
    setattr(user, field, info)
    user.save()
    return user.get_data()


def delete_user(user_id) -> bool:
    try:
        user = User.get(User.id == user_id)
        user.delete_instance(recursive=True)
        cache.set('user_{}_valid'.format(user_id), 'false')
        return True
    except DoesNotExist:
        raise UserNotFound


def update_profile_picture(user_id, profile_picture):
    user = get(user_id)
    if 'filepath' in user.picture:
        former_file_path = user.picture.split('=')[1]
        storage.delete_object(Key=former_file_path, Bucket='template-storage')
    new_picture_id = uuid.uuid4().hex
    file_path = 'profile-pictures/{}'.format(new_picture_id)
    storage.upload_fileobj(profile_picture, 'template-storage', file_path)
    user.picture = '{}/storage/download?filepath={}'.format(config['back_root_url'], file_path)
    user.save()
    profile, account_activated, first_login = user.get_data()

    return {'profile': profile, 'account_activated': account_activated, 'first_login': first_login}
