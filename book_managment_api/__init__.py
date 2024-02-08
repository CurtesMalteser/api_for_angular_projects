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
from book_managment_api.models.book_dto import *

books : list[Book] = []

is_success : bool = True

def create_app(test_config=None):

    app = Flask(__name__, instance_relative_config=True)

    setup_db(app)

    cors = CORS(app, resources={r"*/api/*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
        return response

    @app.route('/books')
    @cross_origin()
    def getBooks():
        if(is_success):
            dataBooks = BookDto.query.all()
            dataBooks = map(lambda  book: Book(
                id= book.bookId,
                title= book.title,
                author= book.author,
                rating= book.rating
            ), dataBooks
            )
            return jsonify(list(dataBooks))
        else:
            abort(404, "Mocked failure! Call GET /success.")

    @app.route('/book', methods=['POST'])
    @cross_origin()
    def addBook():
        if(is_success):
            content_type = request.headers.get('Content-Type')
            if ('application/json' in str(content_type)):
                try:
                    json_data = json.dumps(request.json)
                    book = json.loads(json_data, object_hook = lambda d : Book.fromDict(d = d))

                    books.append(book)

                    return jsonify({
                        "sucess": True
                    })

                except:
                    abort(422, "JSON malformed.")

            else:
                abort(404, "Content type is not supported.")
        else:
            abort(404, "Mocked failure! Call GET /success.")


    @app.route('/book/<string:bookId>', methods=['DELETE'])
    @cross_origin()
    def deleteBook(bookId: str):

        error = False

        try:
            book = BookDto.query.filter_by(bookId=bookId).first()
            if(isinstance(book, BookDto)):
                book.delete()
            else:
                error = True
        except:
            error = True
            db.session.rollback()
        finally:
            db.session.close()
        
        if(error):
            abort(500)
        else:
           return jsonify({
                        "sucess": True
                    })

    @app.route('/success')
    @cross_origin()
    def isSuccess():
        global is_success
        is_success = True
        return jsonify("isSuccess: True")

    @app.route('/failure')
    @cross_origin()
    def isFailure():
        global is_success
        is_success = False
        return jsonify("isSuccess: False")

    return app