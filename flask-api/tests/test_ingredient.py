import time
import json
import unittest
import traceback

from api import db
from api.models.user import User
from tests.base_test_case import BaseTestCase
from tests.helpers.auth import req_user_login, req_user_register, req_user_status
from tests.helpers.ingredient import req_add_ingredient_to_pantry, get_ingredients_from_pantry
from helpers import json_to_ingredient, json_to_user, json_to_recipe
from api.models.user import User
from api.models.ingredient import Ingredient, PantryIngredient


class TestIngredient(BaseTestCase):


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
    icecream = {
        'name': 'icecream',
        'measurement': 'MASS',
        'value': 5.0
    }

    rootbeer = {
        'name': 'rootbeer',
        'measurement': 'VOLUME',
        'value': 5.0
    }

    rootbeer_float = {
        'name': 'Rootbeer Float',
        'ingredients': [rootbeer, icecream],
        'description': 'icecream in rootbeer in cup',
        'steps': ['Place icecream in cup', 'Add rootbeer to cup'],
        'rating': 0.0
    }

    user_obj = {
        'email': 'frankie@reynolds.net',
        'username': 'Frank',
        'password': 'magnum',
        'ingredients': [meat, water]
    }



    def test_add_new_pantry_ingredients(self):

        dbrb = json_to_ingredient(self.rootbeer, access_db=True)
        dbic = json_to_ingredient(self.icecream, access_db=True)
        user = json_to_user(self.user_obj, access_db=True)
        db.session.commit()

        with self.client:
            response = req_user_login(self, 'Frank', 'magnum')
            user_data = json.loads(response.data.decode())
            ingredients_to_quantity = {'rootbeer': 5.0, 'icecream': 3.0}
            response = req_add_ingredient_to_pantry(self, ingredients_to_quantity, user_data)
            data = json.loads(response.data.decode())
            self.assertEqual(data['status'], 'success')
            i = Ingredient.query.filter(Ingredient.name == 'rootbeer').first()
            u = User.query.filter(User.username == 'Frank').first()
            p = PantryIngredient.query.filter((PantryIngredient.user_id == u.id) & (PantryIngredient.ingredient_id == i.id)).first()
            self.assertEqual(p.value, 5.0)

    def test_add_existing_pantry_ingredients(self):

        dbrb = json_to_ingredient(self.rootbeer, access_db=True)
        dbic = json_to_ingredient(self.icecream, access_db=True)
        user = json_to_user(self.user_obj, access_db=True)
        db.session.commit()

        i = Ingredient.query.filter(Ingredient.name == 'rootbeer').first()
        u = User.query.filter(User.username == 'Frank').first()
        pantry_ingredient = PantryIngredient(ingredient=i, user=u, value=11.0)
        db.session.add(pantry_ingredient)

        with self.client:
            response = req_user_login(self, 'Frank', 'magnum')
            user_data = json.loads(response.data.decode())
            ingredients_to_quantity = {'rootbeer': 7.0, 'icecream': 3.0}
            response = req_add_ingredient_to_pantry(self, ingredients_to_quantity, user_data)
            data = json.loads(response.data.decode())
            self.assertEqual(data['status'], 'success')
            ing = Ingredient.query.filter(Ingredient.name == 'rootbeer').first()
            use = User.query.filter(User.username == 'Frank').first()
            pan = PantryIngredient.query.filter((PantryIngredient.user_id == use.id) & (PantryIngredient.ingredient_id == ing.id)).first()
            self.assertEqual(pan.value, 7.0)

    def test_get_ingredients(self):
        dbrb = json_to_ingredient(self.rootbeer, access_db=True)
        dbic = json_to_ingredient(self.icecream, access_db=True)
        user = json_to_user(self.user_obj, access_db=True)
        db.session.commit()

        with self.client:
            response = req_user_login(self, 'Frank', 'magnum')
            user_data = json.loads(response.data.decode())
            ingredients_to_quantity = {'rootbeer': 7.0, 'icecream': 3.0}
            response = req_add_ingredient_to_pantry(self, ingredients_to_quantity, user_data)
            data = json.loads(response.data.decode())
            self.assertEqual(data['status'], 'success')
            response = get_ingredients_from_pantry(self, user_data)
            data = json.loads(response.data.decode())
            self.assertEqual(data['status'], 'success')
            for entry in data['data']['ingredients']:
	            if entry['name'] == 'rootbeer':
	            	 self.assertEqual(entry['value'], 7.0)
	            elif entry['name'] == 'icecream':
	            	 self.assertEqual(entry['value'], 3.0)


if __name__ == '__main__':
    unittest.main()
