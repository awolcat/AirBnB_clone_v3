#!/usr/bin/python3
"""This module defines view functions for Place objects
    as part of the app_views blueprint
    registered to the api app
"""
from flask import request, make_response, abort, jsonify
from models import storage
from models.city import City
from models.place import Place
from api.v1.views import app_views


@app_views.route('/cities/<city_id>/places',
                 strict_slashes=False, methods=['GET', 'POST'])
def get_post_places(city_id):
    """Return a JSON of all places in a city"""
    city_obj = storage.get(City, city_id)
    if city_obj is None:
        abort(404)
    if request.method == 'GET':
        temp = []
        for place in city_obj.places:
            temp.append(place.to_dict())
        return jsonify(temp)
    if request.method == 'POST':
        if request.is_json is False:
            abort(400, "Not a JSON")
        data = request.get_json()
        if data.get("user_id") is None:
            abort(400, "Missing user_id")
        user = data["user_id"]
        if storage.get(User, userId) is None:
            abort(404)
        if data.get("name") is None:
            abort(400, "Missing name")
        new_place = Place()
        data['city_id'] = city_obj.id
        new_place.__dict__.update(data)
        new_place.save()
        return make_response(new_place.to_dict(), 201)


@app_views.route('/places/<place_id>', strict_slashes=False,
                 methods=['GET', 'DELETE', 'PUT'])
def place_by_id(city_id):
    """Return the place identified by <place_id>"""
    the_place = storage.get(Place, place_id)
    if the_place is None:
        abort(404)
    if request.method == 'GET':
        return make_response(the_place.to_dict())
    elif request.method == 'DELETE':
        try:
            storage.delete(the_place)
            storage.save()
        except Exception as e:
            abort(500, e)
        return make_response({})
    elif request.method == 'PUT':
        if request.is_json is False:
            abort(400, "Not a JSON")
        storage.update(Place, the_place.id, request.get_json())
        temp = storage.get(Place, place.id)
        return make_response(temp.to_dict())
