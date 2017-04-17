# manage.py

import os
import unittest
import json

from flask_script import Manager
from sqlalchemy.exc import IntegrityError

from api import app, db, bcrypt

from helpers import json_to_user, json_to_ingredient, json_to_recipe

manager = Manager(app)

@manager.command
def test():
    """Runs the unit tests without test coverage."""
    tests = unittest.TestLoader().discover('tests/', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    else:
        return 1

@manager.command
def create_db():
    """Creates the db tables."""
    db.create_all()


@manager.command
def drop_db():
    """Drops the db tables."""
    db.drop_all()

@manager.command
def seed_sampledata():
    """ Seeds the db with sample data. """
    db.drop_all()
    db.create_all()

    with open('../sampledata/sampleingredients.json') as f:
        contents = json.load(f)
        added = [json_to_ingredient(x, access_db=True) for x in contents['Ingredient']]
        # db.session.add_all(to_add)
        db.session.commit()

    with open('../sampledata/sampleusers.json') as f:
        contents = json.load(f)
        added = [json_to_user(x, access_db=True) for x in contents['Users']]
        # db.session.add_all(to_add)
        db.session.commit()

    with open('../sampledata/samplerecipes.json') as f:
        contents = json.load(f)
        added = [json_to_recipe(x, access_db=True) for x in contents['Recipes']]
        # db.session.add_all(to_add)
        db.session.commit()



if __name__ == "__main__":
    manager.run()
