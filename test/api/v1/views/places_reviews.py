#!/usr/bin/python3
"""Create a states.py"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.review import Review
from models.user import User
from models.place import Place


@app_views.route('/places/<string:place_id>/reviews', methods=['GET'],
                strict_slashes=False)
def reviews(place_id):
    """get all reviews in a list"""
    list_places = storage.get('Place', place_id)
    if list_places is None:
        abort(404)
    list_reviews = []
    for review in list_reviews:
        list_reviews.append(review.to_list_reviews)
    return jsonify(list_reviews)


@app_views.route('/reviews/<string:review_id>', methods=['GET'],
                strict_slashes=False)
def reviewid(review_id):
    idreview = storage.get("Review", review_id)
    if idreview is None:
        abort(404)
    return jsonify(idreview.to_dict())


@app_views.route('/reviews/<string:review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete(review_id):
    """delete Review"""
    idreview = storage.get("Review", review_id)
    if idreview is None:
        abort(404)
    idreview.delete()
    storage.save()
    return (jsonify({}), 200)


@app_views.route('/palces/<string:place_id>/reviews', methods=['POST'],
                strict_slashes=False)
def post(place_id):
    """function or route that create a new Review"""
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    info = request.get_json()
    if 'user_id' not in info:
        return make_response(jsonify({'error': 'Missing user_id'}), 400)
    infoUser = storage.get("User", info['user_id'])
    if infoUser is None:
        abort(404)
    if 'text' not in info:
        return make_response(jsonify({'error': 'Missing text'}), 400)
    info['place_id'] = place_id
    newReview = Review(**info)
    newReview.save()
    return make_response(jsonify(newReview.to_dict()), 201)


@app_views.route('/reviews/<string:review_id>', methods=['PUT'],
                strict_slashes=False)
def put(review_id):
    """function or route that update an Review"""
    idreview = storage.get("Review", review_id)
    if idreview is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for name, value in request.get_json().items():
        if name not in ['id', 'user_id', 'place_id',
                        'created_at', 'updated_at']:
            setattr(idreview, name, value)
        idreview.save()
        return jsonify(idreview.to_dict(), 200)
