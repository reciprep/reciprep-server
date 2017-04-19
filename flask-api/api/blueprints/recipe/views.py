import uuid
from flask import Blueprint, request, make_response, jsonify, g
from flask_restful import Api, Resource, url_for, reqparse

from helpers import recipe_to_json

from api import bcrypt, db
from api.models.user import User
from api.models.recipe import Recipe
from api.models.ingredient import Ingredient, RecipeIngredient, PantryIngredient
from api.decorators import is_logged_in

recipe_blueprint = Blueprint('recipe', __name__)
recipe_api = Api(recipe_blueprint)

class SearchResource(Resource):
    """
    Recipe search resource
    """

    decorators = [is_logged_in]

    # parser = reqparse.RequestParser()
    # parser.add_argument('query', type=str, location='args')

    def get(self):
        """
        Search for ingredients that match the user's criteria and pantry contents

        This method is hacked together and should be completely rewritten.
            Not kidding, it's awful.
                Seriously.
        """

        # args = self.parser.parse_args()
        # query = args['query']
        query = request.args.get('query')

        # user = User.query.filter(User.id == g.user_id).first()
        user = User.query.get(g.user_id)

        # print(user.id)

        # print('Running query')
        # recipes =
        # recipes = Recipe.query.join(Recipe.ingredients.filter(Ingredient.id.in_(User.ingredients))).all()
        # print(len(recipes))
        result = PantryIngredient.query.filter(PantryIngredient.user_id == user.id).all()

        ingredients = {}
        for i in result:
            ingredients[i.ingredient_id.hex] = i.value

        print(ingredients)

        # ingredients = set([i.id for i in user.ingredients])

        # recipes = Recipe.query.filter(set(ingredients.keys()) >= set([i.id for i in Recipe.ingredients])).all()
        result = RecipeIngredient.query.filter(
            # (RecipeIngredient.ingredient_id.in_(ingredients.keys()))
            (RecipeIngredient.ingredient_id.in_(ingredients.keys()))
            # (RecipeIngredient.value <= ingredients[RecipeIngredient.ingredient_id.hex])
        )\
        .all()

        result = [i for i in result if i.value <= ingredients[i.ingredient_id.hex]]
        # .filter(RecipeIngredient.value <= ingredients[RecipeIngredient.ingredient_id.hex])\

        print(result)

        matches = {}
        expected = {}

        for i in result:
            if i.recipe_id.hex in matches:
                matches[i.recipe_id.hex] += 1
            else:
                expected[i.recipe_id.hex] = len(RecipeIngredient.query.filter(RecipeIngredient.recipe_id == i.recipe_id.hex).all())
                matches[i.recipe_id.hex] = 1

        print(matches)
        print(expected)

        recipe_ids = []
        print(recipe_ids)

        # raise Exception

        for key, value in matches:
            if expected[key] <= value:
                recipe_ids.append(key)

        print(recipe_ids)


        recipes = Recipe.query.filter(Recipe.id.in_(recipe_ids))

        print(recipes)


        # print(recipes)

        if query is not None:
            terms = query.split('+')

            # RecipeIngredient.query.filter(RecipeIngredient.ingredient_id.in_(ingredients.keys()))


        else:
            pass

class CreateResource(Resource):
    """
    Recipe creation resource
    """

    decorators = [is_logged_in]

    def post(self):
        pass


class PrepareResource(Resource):
    """
    Preparing a recipe deducts its ingredients from the User's pantry
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
            # recipe = Recipe.query.filter(Recipe.id == recipe_id).first()
            recipe = Recipe.query.get(recipe_id)

            if recipe:
                return make_response(recipe_to_json(recipe), 200)

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
