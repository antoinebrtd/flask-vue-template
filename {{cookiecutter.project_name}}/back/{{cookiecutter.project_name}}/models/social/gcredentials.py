from peewee import *

from {{cookiecutter.project_name}}.core import db
from {{cookiecutter.project_name}}.models.social.user import User


class GCredentials(Model):
    id = PrimaryKeyField()
    user = ForeignKeyField(User, unique=True)
    token = CharField()
    refresh_token = CharField(null=True)
    token_uri = CharField()
    client_id = CharField()
    client_secret = CharField()
    scopes = CharField()

    class Meta:
        database = db


with db:
    GCredentials.create_table(fail_silently=True)
