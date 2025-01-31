#!/usr/bin/python3
"""This module defines a Flask app
    - the Airbnb Clone api"""
import os
from flask import Flask, make_response
from flask_cors import CORS
from models import storage
from api.v1.views import app_views


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown(error):
    """Defines what happens at the end of a request"""
    storage.close()


@app.errorhandler(404)
def page_not_found(error):
    """Custom error message or page"""
    return make_response({"error": "Not found"}, 404)


if __name__ == '__main__':
    host = os.getenv('HBNB_API_HOST') or '0.0.0.0'
    port = os.getenv('HBNB_API_PORT') or 5000
    app.run(host=host, port=port, threaded=True)
