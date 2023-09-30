#!/usr/bin/python3
"""This module defines the blueprint app_views"""
from flask import make_response
from api.v1.views import app_views


@app_views.route('/status')
def api_status():
    """Return a JSON"""
    payload = {'status': 'OK'}
    return make_response(payload)
