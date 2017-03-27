from flask import Blueprint, request, make_response, jsonify, g
from flask_restful import Api, Resource, url_for, reqparse

from api import bcrypt, db
from api.models.user import User
from api.models.recipe import Recipe
from api.models.ingredient import Ingredient
from api.decorators import is_logged_in

recipe_blueprint = Blueprint('recipe', __name__)
recipe_api = Api(recipe_blueprint)

class SearchAPI(Resource):
    """
    Recipe search resource
    """

    decorators = [is_logged_in]

    parser = reqparse.RequestParser()
    parser.add_argument('query')

    def get(self):
        """ Search for ingredients that match the user's criteria and pantry contents """

        args = self.parser.parse_args()
        query = args['query']

        if query is not None:
            terms = query.split('+')
            
        else:
            pass

recipe_api.add_resource(SearchAPI, '/api/recipe/search')