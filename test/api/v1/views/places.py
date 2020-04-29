#!/usr/bin/python3
"""Create a states.py"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.Place import Place
from models.Place import Place
from models.place import place


@app_views.route('/cities/<string:city_id>/places', methods=['GET'],
                strict_slashes=False)
def places(city_id):
    """get all cities in a list"""
    list_cities = storage.get("City", city_id)
    if list_cities is None:
        abort(404)
    list_places = []
    for name in list_cities.places:
        list_places.append(name.to_dict())
    return jsonify(list_places)


@app_views.route('/places/<string:place_id>', methods=['GET'],
                strict_slashes=False)
def placeid(place_id):
    idplace = storage.get("Place", place_id)
    if idplace is None:
        abort(404)
    return jsonify(idplace.to_dict())


@app_views.route('/places/<string:place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete(place_id):
    """delete place"""
    idplace = storage.get("Place", place_id)
    if idplace is None:
        abort(404)
    idplace.delete()
    storage.save()
    return (jsonify({}), 200)


@app_views.route('/cities/<string:place_id>', methods=['POST'],
                strict_slashes=False)
def post():
    """function or route that create a new place"""
    idplace = storage.get("City", city_id)
    if idplace is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    info = request.get_json()
    if 'Place_id' not in info
        return make_response(jsonify({'error': 'Missing Place'}), 400)
    infoPlace = storage.get("Place", info['Place_id'])
    if infoPlace is None:
        abort(404)
    if 'name' not in info:
        return make_response(jsonify({'error': 'Missing name'}), 400)
    info['city_id'] = city_id
    newPlace = Place(**info)
    newPlace.save()
    return make_response(jsonify(newPlace.to_dict()), 201)


@app_views.route('/places/<string:place_id>', methods=['PUT'],
                strict_slashes=False)
def put(place_id):
    """function or route that update an amenity"""
    idplace = storage.get("Place", place_id)
    if idplace is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for name, value in request.get_json().items():
        if name not in ['id', 'user_id','city_id', 'created_at',
                        'updated_at']:
            setattr(place, name, value)
        idplace.save()
        return jsonify(idplace.to_dict(), 200)
