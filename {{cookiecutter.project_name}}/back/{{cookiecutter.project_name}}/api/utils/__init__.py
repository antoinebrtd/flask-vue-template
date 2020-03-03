from flask_app.api import api
from .tree import Tree

api.add_resource(Tree, '/tree')
