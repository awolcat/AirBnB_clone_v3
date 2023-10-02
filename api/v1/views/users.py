#!/usr/bin/python3
"""This module defines view functions for City objects
    as part of the app_views blueprint
    registered to the api app
"""
from flask import request, make_response, abort, jsonify
from models import storage
from models.user import User
from api.v1.views import app_views


@app_views.route('/users', strict_slashes=False, methods=['GET', 'POST'])
def get_post_users():
    """Return a JSON of all users"""
    if request.method == 'GET':
        temp = []
        users_dict = storage.all(User)
        for value in users_dict.values():
            temp.append(value.to_dict())
        return jsonify(temp)
    if request.method == 'POST':
        if request.is_json is False:
            abort(400, "Not a JSON")
        data = request.get_json()
        if data.get("email") is None:
            abort(400, "Missing email")
        elif data.get("password") is None:
            abort(400, "Missing password")
        new_user = User()
        new_user.__dict__.update(data)
        new_user.save()
        return make_response(new_user.to_dict(), 201)


@app_views.route('/users/<user_id>', strict_slashes=False,
                 methods=['GET', 'DELETE', 'PUT'])
def user_by_id(user_id):
    """Return the user identified by <user_id>"""
    the_user = storage.get(User, user_id)
    if the_user is None:
        abort(404)
    if request.method == 'GET':
        return make_response(the_user.to_dict())
    elif request.method == 'DELETE':
        try:
            storage.delete(the_user)
            storage.save()
        except Exception as e:
            abort(500, e)
        return make_response({})
    elif request.method == 'PUT':
        if request.is_json is False:
            abort(400, "Not a JSON")
        storage.update(User, user_id, request.get_json())
        temp = storage.get(User, user_id)
        return make_response(temp.to_dict())
