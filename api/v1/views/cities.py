#!/usr/bin/python3
"""This module defines view functions for City objects
    as part of the app_views blueprint
    registered to the api app
"""
from flask import request, make_response, abort, jsonify
from models import storage
from models.state import State
from models.city import City
from api.v1.views import app_views


@app_views.route('/states/<state_id>/cities', strict_slashes=False, methods=['GET', 'POST'])
def all_states(state_id):
    """Return a JSON of all states"""
    state_obj = storage.get(State, state_id)
    if state_obj is None:
        abort(404)
    if request.method == 'GET':
        temp = []
        state_obj = storage.get(State, state_id)
        for city in state_obj.cities:
            temp.append(city.to_dict())
        return jsonify(temp)
    if request.method == 'POST':
        if request.is_json is False:
            abort(400, "Not a JSON")
        data = request.get_json()
        if data.get("name") is None:
            abort(400, "Missing name")
        new_city = City()
        new_city.__dict__.update(data)
        storage.new(new_city)
        storage.save()
        return make_response(new_city.to_dict(), 201)


@app_views.route('/cities/<city_id>', strict_slashes=False,
                 methods=['GET', 'DELETE', 'PUT'])
def state_by_id(city_id):
    """Return the state identified by <state_id>"""
    the_city = storage.get(City, city_id)
    if the_city is None:
        abort(404)
    if request.method == 'GET':
        return make_response(the_city.to_dict())
    elif request.method == 'DELETE':
        try:
            storage.delete(the_city)
            storage.save()
        except Exception as e:
            abort(500, e)
        return make_response({})
    elif request.method == 'PUT':
        if request.is_json is False:
            abort(400, "Not a JSON")
        storage.update(City, city_id, request.get_json())
        temp = storage.get(City, city_id)
        return make_response(temp.to_dict())
