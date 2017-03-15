from flask_testing import TestCase
from api import app, db

class BaseTestCase(TestCase):
    """
    A base class for running unit tests
    """

    def create_app(self):
        app.config.from_object('api.config.TestingConfig')
        return app

    def setUp(self):
        db.create_all()
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
