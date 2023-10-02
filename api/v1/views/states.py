#!/usr/bin/python3
"""This module defines view functions
    as part of the app_views blueprint
    registered to the api app
"""
from flask import request, make_response, abort, jsonify
from models import storage
from models.state import State
from api.v1.views import app_views


@app_views.route('/states', strict_slashes=False, methods=['GET', 'POST'])
def get_post_states():
    """Return a JSON of all states"""
    if request.method == 'GET':
        temp = []
        objects_dict = storage.all(State)
        for key, value in objects_dict.items():
            temp.append(value.to_dict())
        return jsonify(temp)
    if request.method == 'POST':
        if request.is_json is False:
            abort(400, "Not a JSON")
        data = request.get_json()
        if data.get("name") is None:
            abort(400, "Missing name")
        new_state = State(**data)
        new_state.save()
        return make_response(new_state.to_dict(), 201)


@app_views.route('/states/<state_id>', strict_slashes=False,
                 methods=['GET', 'DELETE', 'PUT'])
def state_by_id(state_id):
    """Return the state identified by <state_id>"""
    the_state = storage.get(State, state_id)
    if the_state is None:
        abort(404)
    if request.method == 'GET':
        return make_response(the_state.to_dict())
    elif request.method == 'DELETE':
        try:
            storage.delete(the_state)
            storage.save()
        except Exception as e:
            abort(500, e)
        return make_response({})
    elif request.method == 'PUT':
        if request.is_json is False:
            abort(400, "Not a JSON")
        storage.update(State, state_id, request.get_json())
        temp = storage.get(State, state_id)
        return make_response(temp.to_dict())
