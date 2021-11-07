#  Copyright (c) Fahad Ahammed 2021.
from src import app
import rq
import redis


class TheRedisQueue:
    def __init__(self):
        self.qrc = redis.Redis(host=app.config.get("REDIS_HOST"), port=app.config.get("REDIS_PORT"), db=app.config.get("REDIS_WORKER_DB"))
        self.q = rq.Queue(connection=self.qrc)