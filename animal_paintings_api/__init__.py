from flask import (
    Flask,
    jsonify,
    send_file,
    abort
    )
from flask_cors import (
    CORS,
    cross_origin,
    )
import json
from animal_paintings_api.models.product import Product
from pathlib import Path

import sys

def create_app(test_config=None):

    app = Flask(__name__, instance_relative_config=True)

    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    file = open('./animal_paintings_api/resources/data.json')
    data = json.load(file, object_hook = lambda d : Product(
        id= str(d.get('id')),
        name= str(d.get('name')),
        price= str(d.get('price')),
        image_url= str(d.get('image_url')),
        ))


    @app.route('/products')
    @cross_origin()
    def getProducts():
        return jsonify(data)


    @app.route('/image/<string:id>')
    @cross_origin()
    def getImage(id: str):
        
        file_name = 'resources/images/{}'.format(id)

        image_file = Path('./animal_paintings_api/{}'.format(file_name))
        if image_file.is_file():
            return send_file(file_name, mimetype='image/jpeg')
        else:
            abort(404)


    return app