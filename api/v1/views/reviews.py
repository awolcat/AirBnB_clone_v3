#!/usr/bin/python3
"""This module defines view functions for City objects
    as part of the app_views blueprint
    registered to the api app
"""
from flask import request, make_response, abort, jsonify
from models import storage
from models.place import Place
from models.review import Review
from api.v1.views import app_views


@app_views.route('/places/<place_id>/reviews',
                 strict_slashes=False, methods=['GET', 'POST'])
def get_post_reviews(place_id):
    """Return a JSON of all reviews of a place"""
    place_obj = storage.get(Place, place_id)
    if place_obj is None:
        abort(404)
    if request.method == 'GET':
        temp = []
        for place in place_obj.reviews:
            temp.append(place.to_dict())
        return jsonify(temp)
    if request.method == 'POST':
        if request.is_json is False:
            abort(400, "Not a JSON")
        data = request.get_json()
        if data.get("user_id") is None:
            abort(400, "Missing user_id")
        if storage.get(User, data.get("user_id")) is None:
            abort(404)
        if data.get("text") is None:
            abort(400, "Missing text")
        new_review = Review()
        data['place_id'] = place_obj.id
        new_review.__dict__.update(data)
        new_review.save()
        return make_response(new_review.to_dict(), 201)


@app_views.route('/reviews/<review_id>', strict_slashes=False,
                 methods=['GET', 'DELETE', 'PUT'])
def review_by_id(review_id):
    """Work with the review identified by <review_id>"""
    the_review = storage.get(Review, review_id)
    if the_review is None:
        abort(404)
    if request.method == 'GET':
        return make_response(the_review.to_dict())
    elif request.method == 'DELETE':
        try:
            storage.delete(the_review)
            storage.save()
        except Exception as e:
            abort(500, e)
        return make_response({})
    elif request.method == 'PUT':
        if request.is_json is False:
            abort(400, "Not a JSON")
        storage.update(Review, review_id, request.get_json())
        temp = storage.get(City, city_id)
        return make_response(temp.to_dict())
