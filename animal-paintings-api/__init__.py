from flask import (
    Flask,
    jsonify,
    )
from flask_cors import (
    CORS,
    cross_origin,
    )
import json


def create_app(test_config=None):

    app = Flask(__name__, instance_relative_config=True)

    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    file = open('./animal-paintings-api/resources/data.json')
    data = json.load(file)


    @app.route('/products')
    @cross_origin()
    def getProducts():
        return jsonify(data)

    return app