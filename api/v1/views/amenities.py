#!/usr/bin/python3
"""This module defines view functions for City objects
    as part of the app_views blueprint
    registered to the api app
"""
from flask import request, make_response, abort, jsonify
from models import storage
from models.amenity import Amenity
from api.v1.views import app_views


@app_views.route('/amenities', strict_slashes=False, methods=['GET', 'POST'])
def get_post_amenities():
    """Return a JSON of all states"""
    if request.method == 'GET':
        temp = []
        amenities_dict = storage.all(Amenity)
        for value in amenities_dict.values():
            temp.append(value.to_dict())
        return jsonify(temp)
    if request.method == 'POST':
        if request.is_json is False:
            abort(400, "Not a JSON")
        data = request.get_json()
        if data.get("name") is None:
            abort(400, "Missing name")
        new_amenity = Amenity()
        new_amenity.__dict__.update(data)
        new_amenity.save()
        return make_response(new_amenity.to_dict(), 201)


@app_views.route('/amenities/<amenity_id>', strict_slashes=False,
                 methods=['GET', 'DELETE', 'PUT'])
def amenity_by_id(amenity_id):
    """Return the state identified by <state_id>"""
    the_amenity = storage.get(Amenity, amenity_id)
    if the_amenity is None:
        abort(404)
    if request.method == 'GET':
        return make_response(the_amenity.to_dict())
    elif request.method == 'DELETE':
        try:
            storage.delete(the_amenity)
            storage.save()
        except Exception as e:
            abort(500, e)
        return make_response({})
    elif request.method == 'PUT':
        if request.is_json is False:
            abort(400, "Not a JSON")
        storage.update(Amenity, amenity_id, request.get_json())
        temp = storage.get(Amenity, amenity_id)
        return make_response(temp.to_dict())
