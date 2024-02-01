from flask import (
    Flask,
    jsonify,
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

    @app.route('/book', methods=['POST'])
    @cross_origin()
    def addBook():
        content_type = request.headers.get('Content-Type')
        if ('application/json' in str(content_type)):
            try:
                json_data = json.dumps(request.json)
                book = json.loads(json_data, object_hook = lambda d : Book.fromDict(d = d))

                books.append(book)

                return jsonify(request.json)

            except:
                abort(422, "JSON malformed.")
        
        else:
            abort(404, "Content type is not supported.")

    return app