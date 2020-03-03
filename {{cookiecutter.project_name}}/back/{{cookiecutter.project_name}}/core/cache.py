from redis import StrictRedis, Redis
from rq import Queue

from .config import config

REDIS_URL = config['cache'].get('url', 'redis://localhost:6379/1')

cache = StrictRedis(
    host=config['cache'].get('host', 'localhost'),
    password=config['cache'].get('password', None),
    db=1, decode_responses=True
)

broker = Redis(
    host=config['cache'].get('host', 'localhost'),
    password=config['cache'].get('password', None),
    db=1
)

queue = Queue(connection=broker, default_timeout=7200)
