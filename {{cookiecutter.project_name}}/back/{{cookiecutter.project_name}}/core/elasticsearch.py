from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth

from .config import config

aws_auth = None

aws_condition = 'localhost' not in config['aws'].get('elastic')
if aws_condition:
    aws_auth = AWS4Auth(config['aws'].get('access_key'), config['aws'].get('private_key'), 'ap-southeast-2', 'es')

es = Elasticsearch([config['aws'].get('elastic')], http_auth=aws_auth, use_ssl=aws_condition,
                   verify_certs=aws_condition,
                   connection_class=RequestsHttpConnection)
