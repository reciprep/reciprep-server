from flask import Blueprint, request, make_response, jsonify, g
from flask.views import MethodView
from flask_restful import Api, Resource, url_for

from api import bcrypt, db
from api.models.user import User
from api.models.recipe import Recipe
from api.models.ingredient import Ingredient
from api.decorators import is_logged_in

recipe_blueprint = Blueprint('recipe', __name__)

class SearchAPI(Resource):
    """
    Recipe search resource
    """

    decorators = [is_logged_in]

    def get(self):
        """ Search for ingredients that match the user's criteria and pantry contents """
