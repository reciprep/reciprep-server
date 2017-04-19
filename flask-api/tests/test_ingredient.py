import time
import json
import unittest

from api import db
from api.models.user import User
from tests.base_test_case import BaseTestCase

from tests.helpers import req_user_login, req_user_register, req_user_status

class TestIngredient(BaseTestCase):
    def test_get_ingredients(self):
        """ Test getting ingredients from user """
        with self.client:
            resp_register = req_user_register(self, 'hammond@ingen.com', 'Richard', 'welcometojp')
            response = req_user_status(self, resp_register.data)
            data = json.loads(response.data.decode())



if __name__ == '__main__':
    unittest.main()
