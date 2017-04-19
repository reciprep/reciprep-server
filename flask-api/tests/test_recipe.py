import time
import json
import unittest
import uuid

from api import db
from api.models.user import User
from api.models.recipe import Recipe
from api.models.ingredient import Ingredient, PantryIngredient, RecipeIngredient
from tests.base_test_case import BaseTestCase

from helpers import json_to_ingredient, json_to_user, json_to_recipe
from tests.helpers.auth import req_user_login, req_user_register, req_user_status
from tests.helpers.recipe import req_recipe_details, req_search_recipe

class TestRecipe(BaseTestCase):
    def test_get_recipe_details(self):
        """ Test for getting a recipe's details """

        meat = {
            'name': 'Meat',
            'measurement': 'MASS',
            'value': 5.0
        }

        water = {
            'name': 'Dirty Water',
            'measurement': 'VOLUME',
            'value': 5.0
        }

        meat_water = {
            'name': 'Meat Water',
            'ingredients': [meat, water],
            'description': 'Watery meat',
            'steps': ['Place meat in bowl', 'Add water'],
            'rating': 0.0
        }

        dbmeat = json_to_ingredient(meat, access_db=True)
        dbwater = json_to_ingredient(water, access_db=True)

        db.session.commit()

        recipe = json_to_recipe(meat_water, access_db=True)

        # HORRIFYING HACK
        meat_water['recipe_id'] = str(uuid.UUID(hex=recipe.id))

        db.session.commit()

        with self.client:
            response = req_recipe_details(self, recipe.id)
            data = json.loads(response.data.decode())

            self.assertEqual(data['status'], 'success')
            self.assertEqual(data['data'], meat_water)
            self.assertEqual(response.status_code, 200)

            response = req_recipe_details(self, 'invalid_id')
            data = json.loads(response.data.decode())

            self.assertEqual(data['status'], 'fail')
            self.assertEqual(response.status_code, 400)

            response = req_recipe_details(self, uuid.uuid4().hex)
            data = json.loads(response.data.decode())

            self.assertEqual(data['status'], 'fail')
            self.assertEqual(response.status_code, 404)


    def test_search_recipes(self):
        """ Test searching for recipes """
        # user = User(
        #     email='hammond@ingen.com',
        #     username='John',
        #     password='welcometojp'
        # )
        #
        # db.session.add(user)

        meat = {
            'name': 'Meat',
            'measurement': 'MASS',
            'value': 5.0
        }

        water = {
            'name': 'Dirty Water',
            'measurement': 'VOLUME',
            'value': 5.0
        }

        meat_water = {
            'name': 'Meat Water',
            'ingredients': [meat, water],
            'description': 'Watery meat',
            'steps': ['Place meat in bowl', 'Add water'],
            'rating': 0.0
        }

        user_obj = {
            'email': 'frankie@reynolds.net',
            'username': 'Frank',
            'password': 'magnum',
            'ingredients': [meat, water]
        }

        dbmeat = json_to_ingredient(meat, access_db=True)
        dbwater = json_to_ingredient(water, access_db=True)
        user = json_to_user(user_obj, access_db=True)

        db.session.commit()

        recipe = json_to_recipe(meat_water, access_db=True)
        db.session.commit()

        with self.client:
            response = req_user_login(self, 'Frank', 'magnum')
            user_data = json.loads(response.data.decode())

            response = req_search_recipe(self, user_data)
            data = json.loads(response.data.decode())
            
            self.assertEqual(data['status'], 'success')

            # response = req_search_recipe(self, )

    def test_create_recipe(self):
        """ Test user creating a recipe """
        pass

    def test_modify_recipe(self):
        """ Test user modifying a recipe """
        pass

    def test_prepare_recipe(self):
        """ Test user cooking a recipe """
        pass




if __name__ == '__main__':
    unittest.main()
