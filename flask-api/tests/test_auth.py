import time
import json
import unittest

from api import db
from api.models.user import User
from tests.base_test_case import BaseTestCase

from tests.helpers.auth import req_user_login, req_user_register, req_user_status

class TestAuth(BaseTestCase):
    def test_register_new_user(self):
        """ Test registering a new user """
        with self.client:
            response = req_user_register(self, 'alan.grant@ingen.com', 'Alan', 'raptors')
            data = json.loads(response.data.decode())

            self.assertEqual(data['status'], 'success')
            self.assertEqual(data['message'], 'Successfully registered.')
            self.assertTrue(data['auth_token'])
            self.assertEqual(response.content_type, 'application/json')
            self.assertEqual(response.status_code, 201)

    def test_user_already_exists(self):
        """ Test if a user can't be registered when they already exist """

        user = User(
            email='hammond@ingen.com',
            username='John',
            password='welcometojp'
        )

        db.session.add(user)
        db.session.commit()

        with self.client:
            response = req_user_register(self, 'hammond@ingen.com', 'Dennis', 'magicword')
            data = json.loads(response.data.decode())

            self.assertEqual(data['status'], 'fail')
            self.assertEqual(data['message'], 'User already exists. Please log in.')
            self.assertEqual(response.content_type, 'application/json')
            self.assertEqual(response.status_code, 202)

            response = req_user_register(self, 'nedry@ingen.com', 'John', 'magicword')
            data = json.loads(response.data.decode())

            self.assertEqual(data['status'], 'fail')
            self.assertEqual(data['message'], 'User already exists. Please log in.')
            self.assertEqual(response.content_type, 'application/json')
            self.assertEqual(response.status_code, 202)


    def test_registered_user_login(self):
        """ Test login for a registered user """

        user = User(
            email='hammond@ingen.com',
            username='John',
            password='welcometojp'
        )

        db.session.add(user)
        db.session.commit()

        with self.client:
            response = req_user_login(self, 'John', 'welcometojp')
            data = json.loads(response.data.decode())
            self.assertEqual(data['status'], 'success')
            self.assertEqual(data['message'], 'Successfully logged in.')
            self.assertTrue(data['auth_token'])
            self.assertEqual(response.content_type, 'application/json')
            self.assertEqual(response.status_code, 200)

    def test_non_registered_user_login(self):
        """ Test for login of non-registered user """
        with self.client:
            response = req_user_login(self, 'Dennis', 'magicword')
            data = json.loads(response.data.decode())
            self.assertEqual(data['status'], 'fail')
            self.assertEqual(data['message'], 'User does not exist.')
            self.assertEqual(response.content_type, 'application/json')
            self.assertEqual(response.status_code, 404)

    def test_get_user_status(self):
        """ Test for getting a user's status """

        with self.client:
            resp_register = req_user_register(self, 'hammond@ingen.com', 'John', 'welcometojp')
            response = req_user_status(self, resp_register.data)
            data = json.loads(response.data.decode())

            self.assertEqual(data['status'], 'success')
            self.assertTrue(data['data'] is not None)
            self.assertEqual(data['data']['email'], 'hammond@ingen.com')
            self.assertEqual(data['data']['username'], 'John')
            self.assertEqual(response.status_code, 200)

    ### TODO implement tests for expired / invalid tokens



if __name__ == '__main__':
    unittest.main()
