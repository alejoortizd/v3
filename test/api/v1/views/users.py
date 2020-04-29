#!/usr/bin/python3
"""Create a states.py"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.user import User


@app_views.route('/amenities', methods=['GET'],
                strict_slashes=False)
def amenities():
    """get all amenitites in a list"""
    list_users = []
    for nameUser in storage.all("User").values():
        list_users.append(nameUser.to_dict())
    return jsonify(list_users)


@app_views.route('/users/<string:user_id>', methods=['GET'],
                strict_slashes=False)
def userid(user_id):
    iduser = storage.get("User", user_id)
    if iduser is None:
        abort(404)
    return jsonify(iduser.to_dict())


@app_views.route('/amenitites/<string:user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete(user_id):
    """delete user"""
    iduser = storage.get("User", user_id)
    if iduser is None:
        abort(404)
    iduser.delete()
    storage.save()
    return (jsonify({}), 200)


@app_views.route('/users', methods=['POST'],
                strict_slashes=False)
def post():
    """function or route that create a new user"""
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'email' not in request.get_json():
        return make_response(jsonify({'error': 'Missing email'}), 400)
        if 'password' not in request.get_json():
        return make_response(jsonify({'error': 'Missing password'}), 400)
    newUser = User(**request.get_json())
    newUser.save()
    return make_response(jsonify(newUser.to_dict()), 201)


@app_views.route('/users/<string:user_id>', methods=['PUT'],
                strict_slashes=False)
def put():
    """function or route that update an amenity"""
    iduser = storage.get("User", user_id)
    if iduser is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for name, value in request.get_json().items():
        if name not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(iduser, name, value)
        iduser.save()
        return jsonify(iduser.to_dict(), 200)
