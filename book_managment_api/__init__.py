from flask import (
    Flask,
    jsonify,
    send_file,
    abort,
    request,
    )
from flask_cors import (
    CORS,
    cross_origin,
    )
import json

def create_app(test_config=None):

    app = Flask(__name__, instance_relative_config=True)

    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    return app