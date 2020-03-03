from peewee import *

from {{cookiecutter.project_name}}.core import db
from {{cookiecutter.project_name}}.models.social.user import User


class FBCredentials(Model):
    id = PrimaryKeyField()
    user = ForeignKeyField(User, unique=True)
    token = CharField()
    fb_user_id = CharField()
    expires_in = IntegerField()
    issued_at = IntegerField()
    scopes = TextField()

    class Meta:
        database = db


with db:
    FBCredentials.create_table(fail_silently=True)
