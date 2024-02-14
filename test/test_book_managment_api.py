# Makes book_managment_api module available,
# if test_book_managment_api.py run from test dir.
import sys
scriptpath = "../"
sys.path.append(scriptpath)

import os
username = os.environ.get('USER', os.environ.get('USERNAME'))
database_name = "bookshelf_test"
database_path = "postgresql://{}:{}@{}/{}".format(username, username,'localhost:5432', database_name)


import unittest
import json
from book_managment_api import create_app
from book_managment_api.models.book_dto import setup_db
import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy


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

        self.new_book = {"id": "sas", "title": "Anansi Boys", "author": "Neil Gaiman", "rating": 5}


    def tearDown(self):
        """Executed after reach test"""
        pass


    # @TODO: Write at least two tests for each endpoint - one each for success and error behavior.
    #        You can feel free to write additional tests for nuanced functionality,
    #        Such as adding a book without a rating, etc.
    #        Since there are four routes currently, you should have at least eight tests.
    # Optional: Update the book information in setUp to make the test database your own!
    def test_add_book_success(self):
        res = self.client().get('/books')
        self.assertEqual(res.status_code, 200)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()