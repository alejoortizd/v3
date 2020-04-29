#!/usr/bin/python3
"""Create a states.py"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'],
                strict_slashes=False)
def states():
    """return in a list all states in the storage"""
    getAllStates = []
    for state in storage.all("State").value():
        getAllStates.append(state.to_dict())
    return jsonify(getAllStates)


@app_views.route('/states/<string:state_id>', methods=['GET'],
                strict_slashes=False)
def stateid(state_id):
    idstate = storage.get("State", state_id)
    if idstate is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<string:state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete(state_id):
    """delete state"""
    idstate = storage.get("State", state_id)
    if idstate is None:
        abort(404)
    idstate.delete()
    storage.save()
    return (jsonify({}), 200)


@app_views.route('/states/', methods=['POST'],
                strict_slashes=False)
def post():
    """function or route that create a new state"""
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'name' not in request.get_json():
        return make_response(jsonify({'error': 'Missing name'}), 400)
    newState = State(**request.get_json())
    newState.save()
    return make_response(jsonify(newState.to_dict()), 201)


@app_views.route('/states/<string:state_id>', methods=['PUT'],
                strict_slashes=False)
def put(state_id):
    """function or route that update a state"""
    idstate = storage.get("State", state_id)
    if idstate is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for name, value in request.get_json().items():
        if name not in ['id', 'created_at', 'updated_at']:
            setattr(idstate, name, value)
        idstate.save()
        return jsonify(idstate.to_dict(), 200)
