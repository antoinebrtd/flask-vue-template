from peewee import PostgresqlDatabase

from .config import config

db = PostgresqlDatabase(
    '{{cookiecutter.project_name}}',
    user=config['database'].get('user'),
    password=config['database'].get('password'),
    host=config['database'].get('host'),
    autorollback=True
)
