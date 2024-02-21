from operator import is_
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

is_success : bool = True

def paginate_books_or_none(request):
    page = request.args.get('page', 1, type=int)
    size = request.args.get('size', 10, type=int)
    size = size if size <= 10 else 10
    start = (page - 1) * size
    end = start + size

    data_books = []
    
    try:
        data_books = BookDto.query.order_by(BookDto.id).all()
    except:
        abort(500)

    total_results = len(data_books)
    data_books = map(lambda  book: Book(
        id= book.bookId,
        title= book.title,
        author= book.author,
        rating= book.rating
    ), data_books
    )

    data_books = list(data_books)[start:end]

    if len(data_books) > 0:
        return jsonify({
            'success': True,
            'books': data_books,
            'page': page,
            'page_size': size,
            'total_results': total_results
            })
    else:
        return None

def create_app(test_config=None):

    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        setup_db(app)
    else:
        config: dict = test_config
        database_path = str(config.get('SQLALCHEMY_DATABASE_URI'))
        setup_db(app, database_path=database_path)

    cors = CORS(app, resources={r"*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
        return response

    @app.route('/books')
    @cross_origin()
    def getBooks():
        if(is_success):
            books = paginate_books_or_none(request=request)

            if books is None:
                abort(400)
            else:
                return books

        else:
            abort(404)

    @app.route('/book', methods=['POST'])
    @cross_origin()
    def addBook():
        if(is_success):
            content_type = request.headers.get('Content-Type')
            if ('application/json' in str(content_type)):
                try:
                    json_data = json.dumps(request.json)
                    book = json.loads(json_data, object_hook = lambda d : Book.fromDict(d = d))

                
                    BookDto(bookId = book.id, title=book.title, author= book.author, rating= book.rating).insert()
                
                    return jsonify(book)

                except:
                    db.session.rollback()
                    abort(422)
                finally:
                    db.session.close()

            else:
                abort(404, "Content type is not supported.")
        else:
            abort(404, "Mocked failure! Call GET /success.")



    @app.route('/book/<string:bookId>', methods=['DELETE'])
    @cross_origin()
    def deleteBook(bookId: str):

        if(is_success):
            error = False

            try:
                book = BookDto.query.filter(BookDto.id == bookId).one_or_none()
                if book is None:
                    error = True
                else:
                    book.delete()
                    
            except:
                error = True
                db.session.rollback()
            finally:
                db.session.close()

            if(error):
                abort(400)
            else:
               return jsonify({
                            "sucess": True,
                            "deleted": bookId,
                        })
        else:
            abort(404, "Mocked failure! Call GET /success.")

    @app.route('/book/<string:book_id>', methods=['PATCH'])
    @cross_origin()
    def update_book_ratomg(book_id: str):
        if(is_success):
            content_type = request.headers.get('Content-Type')
            if ('application/json' in str(content_type)):
                body = request.get_json()
                try:
                    book = BookDto.query.filter(BookDto.id == book_id).one_or_none()

                    if(book is None):
                        abort(404)

                    if('rating' in body):
                        book.rating = int(body.get("rating"))

                    book.update()

                    return jsonify({
                        "sucess": True,
                        "updated": book_id,
                        })

                except:
                    abort(400) 
                        
            else:
                abort(404)
        else:
            abort(404, "Mocked failure! Call GET /success.")

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


    @app.errorhandler(400)
    def not_there(error):
        return jsonify({
            "success": False, 
            "error": 400,
            "message": "Bad request",
            }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False, 
            "error": 404,
            "message": "Not found",
            }), 404


    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False, 
            "error": 422,
            "message": "Unprocessable: {}".format(error),
            }), 422


    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({
            "success": False, 
            "error": 500,
            "message": "Internal Server Error",
            }), 500


    return app