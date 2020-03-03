import json
import os

from flask import request
from flask_restful import Resource


class Tree(Resource):
    def get(self):
        folder = request.args['folder']
        tree = json.load(open(os.environ.get('TREE_FILE', './config/tree.json')))[folder]
        tree = [{
            'id': 0,
            'name': folder,
            'children': tree
        }]

        return {'msg': 'success', 'tree': tree}
