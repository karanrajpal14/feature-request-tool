from flask_testing import TestCase

from app import app, db


class BaseTestCase(TestCase):
    """A base test case"""

    def create_app(self):
        app.config.from_object("config.TestingConfig")
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
