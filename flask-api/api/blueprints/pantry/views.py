from flask import Blueprint, request, make_response, jsonify, g
from flask.views import MethodView
from flask_restful import Api, Resource, url_for

from api import bcrypt, db
from api.models.user import User
from api.models.ingredient import Ingredient
from api.decorators import is_logged_in

pantry_blueprint = Blueprint('pantry', __name__)
pantry_api = Api(pantry_blueprint)

class IngredientsAPI(Resource):
    """
    Resources for managing ingredients in the User's pantry
    """
    decorators = [is_logged_in]

    def post(self):
        """ Add a new ingredient to the pantry """
        pass

    def delete(self):
        """ Remove an ingredient from the pantry """
        pass

    def patch(self):
        """ Change the amount of an ingredient in the pantry """
        pass

    def get(self):
        """ Get a list all of the ingredients, with the ones in the pantry marked """
        pass

pantry_api.add_resource(IngredientsAPI, '/api/pantry/ingredients')
