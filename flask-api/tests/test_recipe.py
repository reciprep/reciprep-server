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
from tests.helpers.recipe import req_recipe_details, req_search_recipe, req_create_recipe, req_prepare_recipe, req_rate_recipe

class TestRecipe(BaseTestCase):
    def test_get_recipe_details(self):
        """ Test for getting a recipe's details, creates a recipe with
        corresponding ingredients, creates an HTTP request and returns
        the result of finding the details of the recipe  """

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
            'rating': None,
            'creator': ''
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
        """ Establishes multiple recipes, creates a request to search through
        the recipes and return specific terms, verifeis that a specific recipe
        is returned"""

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

        dog_food = {
            'name': 'Dog Food',
            'measurement': 'MASS',
            'value': 5.0
        }

        meat_water = {
            'name': 'Meat Water',
            'ingredients': [meat, water],
            'description': 'Watery meat',
            'steps': ['Place meat in bowl', 'Add water'],
            'rating': 1.0
        }

        dog_food_recipe = {
            'name': 'Dog Food Recipe',
            'ingredients': [dog_food],
            'description': 'This is for dogs. Do not eat.',
            'steps': ['Place in dog bowl.', 'Consume.'],
            'rating': 3.0
        }

        user_obj = {
            'email': 'frankie@reynolds.net',
            'username': 'Frank',
            'password': 'magnum',
            'ingredients': [meat, water]
        }

        dbmeat = json_to_ingredient(meat, access_db=True)
        dbwater = json_to_ingredient(water, access_db=True)
        dbdog_food = json_to_ingredient(dog_food, access_db=True)
        user = json_to_user(user_obj, access_db=True)

        db.session.commit()

        recipe = json_to_recipe(meat_water, access_db=True)
        df_recipe = json_to_recipe(dog_food_recipe, access_db=True)
        db.session.commit()

        meat_water_simple = {
            'name': 'Meat Water',
            'description': 'Watery meat',
            'rating': 1.0
        }

        dog_food_simple = {
            'name': 'Dog Food Recipe',
            'description': 'This is for dogs. Do not eat.',
            'rating': 3.0
        }

        meat_water_simple['recipe_id'] = str(uuid.UUID(hex=recipe.id.hex))


        with self.client:
            response = req_user_login(self, 'Frank', 'magnum')
            user_data = json.loads(response.data.decode())

            response = req_search_recipe(self, user_data, filter_='true')
            data = json.loads(response.data.decode())

            self.assertEqual(data['status'], 'success')
            self.assertEqual(data['data']['recipes'], [meat_water_simple])

            response = req_search_recipe(self, user_data, 'meat water', filter_='true')
            data = json.loads(response.data.decode())

            self.assertEqual(data['status'], 'success')
            self.assertEqual(data['data']['recipes'], [meat_water_simple])

            response = req_search_recipe(self, user_data, 'random query', filter_='true')
            data = json.loads(response.data.decode())

            self.assertEqual(data['status'], 'success')
            self.assertEqual(data['data']['recipes'], [])

            response = req_search_recipe(self, user_data)
            data = json.loads(response.data.decode())

            self.assertEqual(data['status'], 'success')
            # print(data['data']['recipes'])
            self.assertEqual(len(data['data']['recipes']), 2)

    def test_create_recipe(self):
        """ Creates a new recipe, sends a request to create the new recipe
        and verifies the result is seen in the backend"""

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

        with self.client:
            response = req_user_login(self, 'Frank', 'magnum')
            user_data = json.loads(response.data.decode())

            response = req_create_recipe(self, user_data, meat_water)
            data = json.loads(response.data.decode())

            self.assertEqual(data['status'], 'success')

            response = req_create_recipe(self, user_data, meat_water)
            data = json.loads(response.data.decode())

            self.assertEqual(data['status'], 'fail')



    def test_modify_recipe(self):
        """ Test user modifying a recipe """
        pass

    def test_prepare_recipe(self):
        """Creates a recipe with multiple ingredients, sends the recipe ID in a
        request. Verifeis that the correct ingredietns are taken out of the
        database for the user"""
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

        dog_food = {
            'name': 'Dog Food',
            'measurement': 'MASS',
            'value': 5.0
        }

        meat_water = {
            'name': 'Meat Water',
            'ingredients': [meat, water],
            'description': 'Watery meat',
            'steps': ['Place meat in bowl', 'Add water'],
            'rating': 1.0
        }

        dog_food_recipe = {
            'name': 'Dog Food Recipe',
            'ingredients': [dog_food],
            'description': 'This is for dogs. Do not eat.',
            'steps': ['Place in dog bowl.', 'Consume.'],
            'rating': 3.0
        }

        user_obj = {
            'email': 'frankie@reynolds.net',
            'username': 'Frank',
            'password': 'magnum',
            'ingredients': [meat, water]
        }

        dbmeat = json_to_ingredient(meat, access_db=True)
        dbwater = json_to_ingredient(water, access_db=True)
        dbdog_food = json_to_ingredient(dog_food, access_db=True)
        user = json_to_user(user_obj, access_db=True)

        db.session.commit()

        recipe = json_to_recipe(meat_water, access_db=True)
        df_recipe = json_to_recipe(dog_food_recipe, access_db=True)
        db.session.commit()

        with self.client:
            response = req_user_login(self, 'Frank', 'magnum')
            user_data = json.loads(response.data.decode())

            response = req_prepare_recipe(self, user_data, recipe)
            data = json.loads(response.data.decode())

            self.assertEqual(data['status'], 'success')
            self.assertEqual(data['has_all_ingredients'], True)

            response = req_prepare_recipe(self, user_data, recipe)
            data = json.loads(response.data.decode())

            self.assertEqual(data['status'], 'fail')


    def test_rate_recipe(self):
        """Create a new recipe and send a request to add a review to it. Verify
        that the review properly updated the rating the appropraite amount"""
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

        dog_food = {
            'name': 'Dog Food',
            'measurement': 'MASS',
            'value': 5.0
        }

        meat_water = {
            'name': 'Meat Water',
            'ingredients': [meat, water],
            'description': 'Watery meat',
            'steps': ['Place meat in bowl', 'Add water'],
        }

        frank_obj = {
            'email': 'frankie@reynolds.net',
            'username': 'Frank',
            'password': 'magnum',
            'ingredients': [meat, water]
        }

        dennis_obj = {
            'email': 'dennis@reynolds.net',
            'username': 'Dennis',
            'password': 'mistertibbs',
            'ingredients': [meat, water]
        }

        dbmeat = json_to_ingredient(meat, access_db=True)
        dbwater = json_to_ingredient(water, access_db=True)
        frank = json_to_user(frank_obj, access_db=True)
        dennis = json_to_user(dennis_obj, access_db=True)

        db.session.commit()

        recipe = json_to_recipe(meat_water, access_db=True)
        db.session.commit()

        with self.client:
            response = req_user_login(self, 'Frank', 'magnum')
            user_data = json.loads(response.data.decode())

            response = req_rate_recipe(self, user_data, recipe, 5.0)
            data = json.loads(response.data.decode())

            self.assertEqual(data['status'], 'success')
            self.assertEqual(recipe.rating, 5.0)

            response = req_rate_recipe(self, user_data, recipe, 1.0)
            data = json.loads(response.data.decode())

            self.assertEqual(data['status'], 'success')
            self.assertEqual(recipe.rating, 1.0)

            response = req_user_login(self, 'Dennis', 'mistertibbs')
            user_data = json.loads(response.data.decode())

            response = req_rate_recipe(self, user_data, recipe, 5.0)
            data = json.loads(response.data.decode())

            self.assertEqual(data['status'], 'success')
            self.assertEqual(recipe.rating, 3.0)


if __name__ == '__main__':
    unittest.main()
