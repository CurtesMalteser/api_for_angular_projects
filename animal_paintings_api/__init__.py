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
from animal_paintings_api.models.product import Product
from pathlib import Path

cart: list[Product] = []

def create_app(test_config=None):

    app = Flask(__name__, instance_relative_config=True)

    cors = CORS(app, resources={r"*/api/*": {"origins": "*"}})

    file = open('./animal_paintings_api/resources/data.json')
    data = json.load(file, object_hook = lambda d : Product.fromDict(d = d))


    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
        return response

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

    @app.route('/cart', methods=['POST'])
    @cross_origin()
    def addToCart():
        content_type = request.headers.get('Content-Type')
        if ('application/json' in str(content_type)):
            try:
                json_data = json.dumps(request.json)
                product = json.loads(json_data, object_hook = lambda d : Product.fromDict(d = d))

                cart.append(product)

                return jsonify(request.json)

            except:
               abort(422, "JSON malformed.")

        else:
            abort(404, "Content type is not supported.")


    @app.route('/cart')
    @cross_origin()
    def getCart():
        return jsonify(cart)

    @app.route('/cart', methods=['DELETE'])
    @cross_origin()
    def clearCart():
        cart.clear()
        return jsonify(success=True), 200
 
    @app.route('/checkout', methods=['POST'])
    @cross_origin()
    def checkout():
        content_type = request.headers.get('Content-Type')
        if ('application/json' in str(content_type)):
            try:
                json_data = json.dumps(request.json)
                json.loads(json_data, object_hook = lambda d : Product.fromDict(d = d))

                cart.clear()

                return jsonify(success=True), 200

            except Exception:
               abort(422, "JSON malformed.")

        else:
            abort(404, "Content type is not supported.")

    return app