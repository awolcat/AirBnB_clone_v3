#!/usr/bin/python3
"""This module defines the blueprint app_views"""
from flask import make_response
from api.v1.views import app_views
from models import storage
from models.user import User
from models.state import State
from models.review import Review
from models.place import Place
from models.city import City
from models.amenity import Amenity


classes = {'users': User, 'states': State, 'reviews': Review, 'places': Place,
        'cities': City, 'amenities': Amenity}
@app_views.route('/status')
def api_status():
    """Return a JSON"""
    payload = {'status':'OK'}
    return make_response(payload)


@app_views.route('/stats')
def statistics():
    """Return object stats"""
    temp = {}
    for key, value in classes.items():
        temp[key] = storage.count(cls=value)
    return make_response(temp)
