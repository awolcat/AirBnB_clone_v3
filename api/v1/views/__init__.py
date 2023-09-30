#!/usr/bin/python3
"""This modules creates an instance of the app_views blueprint"""
from flask import Blueprint


app_views = Blueprint('/api/v1', __name__, url_prefix='/api/v1')


from api.v1.views import index
from api.v1.views.index import *
