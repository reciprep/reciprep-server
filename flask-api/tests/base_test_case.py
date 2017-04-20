from flask_testing import TestCase, LiveServerTestCase
from api import app, db


class BaseTestCase(TestCase):
    """
    A base class for running unit tests
    """

    def create_app(self):
        app.config.from_object('api.config.TestingConfig')
        return app

    def setUp(self):
        db.drop_all()
        db.configure_mappers()
        db.create_all()
        # db.seed_sampledata()
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

class LiveBaseTestCase(LiveServerTestCase):
    """
    A base class for running unit tests on a live server
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
