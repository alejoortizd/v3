#!/usr/bin/python3
"""Create a states.py"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'],
                strict_slashes=False)
def amenities():
    """get all amenitites in a list"""
    list_amenities = []
    for nameAmenity in storage.all("Amenity").values():
        list_amenities.append(nameAmenity.to_dict())
    return jsonify(list_amenities)


@app_views.route('/amenities/<string:amenity_id>', methods=['GET'],
                strict_slashes=False)
def amenityid(amenity_id):
    idamenity = storage.get("Amenity", amenity_id)
    if idamenity is None:
        abort(404)
    return jsonify(idamenity.to_dict())


@app_views.route('/amenitites/<string:amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete(amenity_id):
    """delete amenity"""
    idamenity = storage.get("Amenity", amenity_id)
    if idamenity is None:
        abort(404)
    idamenity.delete()
    storage.save()
    return (jsonify({}), 200)


@app_views.route('/amenities', methods=['POST'],
                strict_slashes=False)
def post():
    """function or route that create a new amenity"""
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'name' not in request.get_json():
        return make_response(jsonify({'error': 'Missing name'}), 400)
    newAmenity = Amenity(**request.get_json())
    newAmenity.save()
    return make_response(jsonify(newAmenity.to_dict()), 201)


@app_views.route('/amenities/<string:amenity_id>', methods=['PUT'],
                strict_slashes=False)
def put():
    """function or route that update an amenity"""
    idamenity = storage.get("Amenity", amenity_id)
    if idamenity is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for name, value in request.get_json().items():
        if name not in ['id', 'created_at', 'updated_at']:
            setattr(idamenity, name, value)
        idamenity.save()
        return jsonify(idamenity.to_dict(), 200)
