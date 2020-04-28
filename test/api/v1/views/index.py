#!/usr/bin/python3
"""create a file index.py"""
from flask import jsonify
from api.v1.views import app_views
from models import storage


"""Create a global dict"""
dcon = {
    "amenities": "Amenity",
    "cities": "City",
    "places": "Place",
    "reviews": "Review",
    "states": "State",
    "users": "User"
}

@app_views.route('/status', strict_slaches=False)
def status():
    """Status"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', strict_slaches=False)
def stats():
    """Stats"""
    ddict = {}
    for name, value in dcon.items():
        ddict[name] = storage.count(value)
    return jsonify(ddict)

if __name__ == "__main__":
    pass
