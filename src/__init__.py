#  Copyright (c) Fahad Ahammed 2021.
import os
from datetime import timedelta

from flask import Flask
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config["THREADED"] = True
app.config["API_VERSION"] = os.environ.get("API_VERSION", "v1")
app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY", "TheDead_Fr0gfellDown...Her3")
ACCESS_EXPIRES = timedelta(hours=int(os.environ.get("JWT_ACCESS_TOKEN_EXPIRES", 1)))
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = ACCESS_EXPIRES
app.config["REDIS_HOST"] = os.environ.get("REDIS_HOST", "127.0.0.1")
app.config["REDIS_PORT"] = int(os.environ.get("REDIS_PORT", 6379))
app.config["REDIS_DB"] = int(os.environ.get("REDIS_DB", 0))
app.config["REDIS_DB_FOR_APP"] = int(os.environ.get("REDIS_DB", 2))
app.config["REDIS_WORKER_DB"] = int(os.environ.get("REDIS_WORKER_DB", 1))
app.config["MONGO_DB_NAME"] = os.environ.get("MONGO_DB_NAME", "NelectMon")
app.config["MONGO_DB_HOST"] = os.environ.get("MONGO_DB_HOST", "127.0.0.1")
app.config["MONGO_DB_PORT"] = int(os.environ.get("MONGO_DB", 27017))
app.config["DEBUG"] = os.environ.get("DEBUG", True)
app.config["HOST"] = os.environ.get("HOST", "0.0.0.0")
app.config["PORT"] = int(os.environ.get("PORT", 11000))

jwt = JWTManager(app)


from src.view.auth import *
from src.view.default import *
