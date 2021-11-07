#  Copyright (c) Fahad Ahammed 2021.
import redis
from src import app


class RedisOps:
    def __init__(self):
        self.rh = app.config.get("REDIS_HOST")
        self.rp = app.config.get("REDIS_PORT")
        self.rd = app.config.get("REDIS_DB_FOR_APP")
        pool = redis.ConnectionPool(host=self.rh, port=int(self.rp),
                                    db=int(self.rd))
        self.rc = redis.Redis(connection_pool=pool, decode_responses=True)

import redis


def insert_data(the_key, the_value):
    r = redis.Redis(host='localhost', port=6379, db=0)
    return r.set(the_key, the_value)


pool = redis.ConnectionPool(host='localhost', port=6379, db=0)

def insert_data(the_key, the_value):
    r = redis.Redis(connection_pool=pool, decode_responses=True)
    return r.set(the_key, the_value)