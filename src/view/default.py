#  Copyright (c) Fahad Ahammed 2021.
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


@app.route(f"/api/{app.config.get('API_VERSION')}/note", methods=["POST"])
@jwt_required()
def insert_note():
    rqj = request.json
    identity = get_jwt_identity()
    return DefaultModel().insert_note(note=rqj.get("note"), email=identity.get("email"))


@app.route(f"/api/{app.config.get('API_VERSION')}/notes", methods=["GET"])
def notes():
    all_notes = DefaultModel().get_notes()
    if all_notes:
        return {'status': 'success', 'data': all_notes, 'msg': 'Notes retrieved successfully'}
    else:
        return {'status': 'failure', 'data': [], 'msg': 'No notes found'}


@app.route(f"/api/{app.config.get('API_VERSION')}/note", methods=["GET"])
def note():
    all_notes = DefaultModel().get_notes()
    note_id = request.args.get('id')
    if all_notes:
        return {'status': 'success', 'data': [x for x in all_notes if x.get("id") == note_id], 'msg': f'Note:{note_id} retrieved successfully'}
    else:
        return {'status': 'failure', 'data': [], 'msg': f'Note:{note_id} not found'}