from os import name
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

from book_managment_api.models.book import Book

books : list[Book] = []

def create_app(test_config=None):

    app = Flask(__name__, instance_relative_config=True)

    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    @app.route('/books')
    @cross_origin()
    def getBooks():
        return jsonify(books)

    return app