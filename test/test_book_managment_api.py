# Makes book_managment_api module available,
# if test_book_managment_api.py run from test dir, since the scriptpath is a relative path.
import sys
scriptpath = "../"
sys.path.append(scriptpath)

import os
username = os.environ.get('USER', os.environ.get('USERNAME'))
database_name = "bookshelf_test"
database_path = "postgresql://{}:{}@{}/{}".format(username, username,'localhost:5432', database_name)


import unittest
from book_managment_api import create_app
from book_managment_api.models.book_dto import BookDto, db
import os
import unittest
import json

def withContext(app, func):
    with app.app_context():
        func()

def setUpDb():
    books = [
        BookDto(bookId="1",title="Book 1",author= "Author 1",rating= 1),
        BookDto(bookId="2",title="Book 2",author= "Author 2",rating= 2),
        BookDto(bookId="3",title="Book 3",author= "Author 3",rating= 3),
        BookDto(bookId="4",title="Book 4",author= "Author 4",rating= 4),
        BookDto(bookId="5",title="Book 5",author= "Author 5",rating= 5),
        BookDto(bookId="6",title="Book 6",author= "Author 6",rating= 6),
        BookDto(bookId="7",title="Book 7",author= "Author 7",rating= 7),
        BookDto(bookId="8",title="Book 8",author= "Author 8",rating= 8),
        BookDto(bookId="9",title="Book 9",author= "Author 9",rating= 9),
        BookDto(bookId="10",title="Book 10",author= "Author 10",rating= 10),
        BookDto(bookId="11",title="Book 11",author= "Author 11",rating= 11),
        ]

    db.session.add_all(books)
    db.session.commit()
    db.session.close()

def tearDownDb():
    db.drop_all()
    db.session.close()

class BookManagementApiTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.database_name = database_name
        self.database_path = database_path
        self.app = create_app({
            "SQLALCHEMY_DATABASE_URI": self.database_path
        })

        self.client = self.app.test_client

        withContext(self.app, func=setUpDb)


    def tearDown(self):
        withContext(self.app, tearDownDb)
        pass

    def test_get_books_success(self):
        res = self.client().get('/books')

        self.assertEqual(res.status_code, 200)

    def test_get_books_pagination(self):
        res = self.client().get('/books?page=2')
        self.assertEqual(res.status_code, 200)

    def test_get_books_max_books_size_success(self):
        res = self.client().get('/books?page=1&size=100')
        jsonData = json.dumps(res.json)
        data = json.loads(jsonData)
        books = list(data.get('books'))

        self.assertEqual(10, len(books))


if __name__ == "__main__":
    unittest.main()