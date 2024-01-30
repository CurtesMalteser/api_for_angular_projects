from flask import (
    Flask,
    jsonify,
    )
from flask_cors import (
    CORS,
    cross_origin,
    )
import json
from animal_paintings_api.models.product import Product

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

    return app