import uuid
from flask import Blueprint, request, make_response, jsonify, g
from flask_restful import Api, Resource, url_for, reqparse

from api import bcrypt, db
from api.models.user import User
from api.models.recipe import Recipe
from api.models.ingredient import Ingredient, RecipeIngredient
from api.decorators import is_logged_in

recipe_blueprint = Blueprint('recipe', __name__)
recipe_api = Api(recipe_blueprint)

class SearchResource(Resource):
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

class CreateResource(Resource):
    """
    Recipe creation resource
    """

    decorators = [is_logged_in]

    def post(self):
        pass


class CookResource(Resource):
    """
    Cooking a recipe deducts its ingredients from the User's pantry
    """

    decorators = [is_logged_in]

    def get(self):
        pass


class ModifyResource(Resource):
    """
    Recipe modification resource
    """
    decorators = [is_logged_in]

    def patch(self, recipe_id):
        pass

    def delete(self, recipe_id):
        pass

class DetailsResource(Resource):
    """
    Recipe details resource
    """
    def get(self, recipe_id):
        try:
            uuid.UUID(hex=recipe_id)
            recipe = Recipe.query.filter(Recipe.id == recipe_id).first()

            if recipe:
                ingredients = RecipeIngredient.query.filter(RecipeIngredient.recipe_id == recipe.id)
                ingredientsObject = [{'name': i.ingredient.name, 'type': i.ingredient.measurement, 'value': i.value} for i in ingredients]

                responseObject = {
                    'status': 'success',
                    'data': {
                        'recipe_id': recipe.id,
                        'name': recipe.name,
                        'ingredients': ingredientsObject,
                        'description': recipe.description,
                        'steps': recipe.steps,
                        'rating': recipe.rating
                    }
                }
                return make_response(jsonify(responseObject), 200)

            else:
                responseObject = {
                    'status': 'fail',
                    'message': 'Recipe %s not found' % recipe_id
                }
                return make_response(jsonify(responseObject), 404)

        except ValueError:
            responseObject = {
                'status': 'fail',
                'message': '%s is not a valid recipe id' % recipe_id
            }
            return make_response(jsonify(responseObject), 400)


recipe_api.add_resource(SearchResource, '/api/recipe/search')
recipe_api.add_resource(CreateResource, '/api/recipe')
recipe_api.add_resource(ModifyResource, '/api/recipe/<string:recipe_id>')
recipe_api.add_resource(DetailsResource, '/api/recipe/<string:recipe_id>')
