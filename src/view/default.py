#  Copyright (c) Fahad Ahammed 2021.
import json

from src import app
from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.model.default import DefaultModel


from src.library.theredisqueue import TheRedisQueue


def tt(delay):
    import time
    print("Inside the function")
    time.sleep(delay)
    print("operation done")
    return delay


# A blocklisted access token will not be able to access this any more
@app.route(f"/api/{app.config.get('API_VERSION')}/protected", methods=["GET"])
@jwt_required()
def protected():
    TheRedisQueue().q.enqueue(tt, delay=5)
    qc = TheRedisQueue().q.count
    return jsonify(total_queue=qc)


def the_caller(data):
    return DefaultModel().insert_beat(data)


@app.route(f"/api/{app.config.get('API_VERSION')}/post_beat", methods=["POST"])
def post_beat():
    data = request.json
    TheRedisQueue().q.enqueue(the_caller, kwargs={"data": data})
    qc = TheRedisQueue().q.count
    return jsonify(total_queue=qc)


@app.route(f"/api/{app.config.get('API_VERSION')}/get_beat", methods=["POST"])
def get_beat():
    data = request.json
    return jsonify(DefaultModel().get_beats(data=data))