import uuid
import math
import traceback
from flask import Blueprint, request, make_response, jsonify, g
from flask_restful import Api, Resource, url_for, reqparse

from helpers import recipe_to_json, json_to_recipe

from api import bcrypt, db
from api.models.user import User
from api.models.recipe import Recipe
from api.models.rating import Rating
from api.models.ingredient import Ingredient, RecipeIngredient, PantryIngredient
from api.decorators import is_logged_in

recipe_blueprint = Blueprint('recipe', __name__)
recipe_api = Api(recipe_blueprint)

class SearchResource(Resource):
    """
    Resource to Search for recipes that match the user's search criteria
    """

    decorators = [is_logged_in]

    def get(self):
        """
        Search for ingredients that match the user's criteria and pantry contents
        Gets the user ID from the auth token. Then it filters for the ingredients
        of the User of the auth token. It then finds the recipes the user can make
        this is sent as a response back to the front end
        """

        query = request.args.get('terms')
        filter_ = request.args.get('filter')

        if filter_ == 'true':
            user = User.query.get(g.user_id)
            result = PantryIngredient.query.filter(PantryIngredient.user_id == user.id).all()

            ingredients = {}
            for i in result:
                ingredients[i.ingredient_id.hex] = i.value

            result = RecipeIngredient.query.filter(
                (RecipeIngredient.ingredient_id.in_(ingredients.keys()))
            )\
            .all()

            result = [i for i in result if i.value <= ingredients[i.ingredient_id.hex]]

            matches = {}
            expected = {}

            for i in result:
                if i.recipe_id.hex in matches:
                    matches[i.recipe_id.hex] += 1
                else:
                    expected[i.recipe_id.hex] = len(RecipeIngredient.query.filter(RecipeIngredient.recipe_id == i.recipe_id.hex).all())
                    matches[i.recipe_id.hex] = 1

            recipe_ids = []

            for key in matches:
                if expected[key] <= matches[key]:
                    recipe_ids.append(key)

            if query:
                recipes = Recipe.query \
                    .filter(Recipe.id.in_(recipe_ids)) \
                    .search(query.replace('+', ' ')) \
                    .all()
            else:
                recipes = Recipe.query.filter(Recipe.id.in_(recipe_ids)).all()

            [recipe_to_json(r, make_json=False, verbose=False) for r in recipes]

            responseObject = {
                'status': 'success',
                'data': {
                    'recipes': [recipe_to_json(r, make_json=False, verbose=False) for r in recipes]
                }
            }

            return make_response(jsonify(responseObject), 200)

        else:
            if query:
                recipes = Recipe.query.search(query.replace('+', ' ')).all()
            else:
                recipes = Recipe.query.all()

            responseObject = {
                'status': 'success',
                'data': {
                    'recipes': [recipe_to_json(r, make_json=False, verbose=False) for r in recipes]
                }
            }

            return make_response(jsonify(responseObject), 200)

class RateResource(Resource):
    """
    Resource to handle Rating Recipes
    """

    decorators = [is_logged_in]

    """
    PUT request takes a recipe id and retrieves the recipe from the database.
    It then takes the review from the front end and averages the score into the
    recipe. The new result is sent back to the frontend
    """
    def put(self, recipe_id):
        try:
            put_data = request.get_json()
            recipe = Recipe.query.get(recipe_id)

            if not recipe:
                responseObject = {
                    'status': 'fail',
                    'message': 'Recipe %s not found.' % recipe_id
                }
                return make_response(jsonify(responseObject), 404)

            value = float(put_data['value'])

            rating = Rating.query.filter(Rating.user_id == g.user_id, Rating.recipe_id == recipe.id).first()

            if rating:
                new_value = (recipe.rating * recipe.num_ratings - recipe.rating + value) / recipe.num_ratings
                rating.value = value
                recipe.rating = new_value
                db.session.commit()

            else:
                rating = Rating(user=g.user, recipe=recipe, value=value)
                db.session.add(rating)

            #### POTENTIAL RACE CONDITIONS ###
                if recipe.num_ratings == 0:
                    recipe.num_ratings = 1
                    recipe.rating = value
                else:
                    new_rating = (recipe.rating * recipe.num_ratings + value) / (recipe.num_ratings + 1)
                    recipe.rating = new_rating
                    recipe.num_ratings = recipe.num_ratings + 1
                db.session.commit()

            responseObject = {
                'status': 'success'
            }

            return make_response(jsonify(responseObject), 200)

        except KeyError:
            responseObject = {
                'status': 'fail',
                'message': 'No rating specified'
            }
            return make_response(jsonify(responseObject), 400)
        except ValueError:
            responseObject = {
                'status': 'fail',
                'message': 'Invalid rating value'
            }
            return make_response(jsonify(responseObject), 400)
        except Exception as e:
            print(e)
            traceback.print_exc()


class CreateResource(Resource):
    """
    Resource to Create a new Recipe
    """

    decorators = [is_logged_in]

    """
    POST request that takes recipe data from the front end. Given a Name,
    Rating, Descriptions, Steps the result is committed into the backend.
    """
    def post(self):
        try:
            post_data = request.get_json()
            if 'rating' in post_data:
                post_data['rating'] = None

            recipe = Recipe.query.filter(Recipe.name == post_data['name']).first()

            if not recipe:
                recipe = json_to_recipe(post_data, creator=g.user)
                db.session.commit()

                responseObject = {
                    'status': 'success',
                    'recipe_id': recipe.id.hex
                }

                return make_response(jsonify(responseObject), 200)
            else:
                responseObject = {
                    'status': 'fail',
                    'message': 'Recipe with name %s already exists.' % recipe.name
                }
                return make_response(jsonify(responseObject), 202)

        except KeyError:
            responseObject = {
                'status': 'fail',
                'message': 'Invalid recipe information provided.'
            }

            return make_response(jsonify(responseObject), 400)


class PrepareResource(Resource):
    """
    Preparing a recipe deducts its ingredients from the User's pantry
    """

    decorators = [is_logged_in]
    """
    Given a Recipe ID query the database for a recipe, go through the ingredients
    and verify they exist in the user's pantry. Once that is verifeid remove the
    ingredients from their pantry
    """
    def put(self, recipe_id):
        user = g.user
        user_id = g.user_id

        recipe = Recipe.query.get(recipe_id)

        if recipe_id is None:
            responseObject = {
                'status': 'fail',
                'message': 'Recipe does not exist.'
            }

            return make_response(jsonify(responseObject), 404)

        recipe_ingredients = RecipeIngredient.query.filter(RecipeIngredient.recipe_id == recipe.id).all()
        user_ingredients = PantryIngredient.query.filter(PantryIngredient.user_id == user_id).all()

        user_dict = {}

        for ui in user_ingredients:
            user_dict[ui.ingredient_id] = ui

        has_all_ingredients = True
        changed = []

        for ri in recipe_ingredients:
            ui = user_dict.get(ri.ingredient_id)
            if ui:
                if math.isclose(ui.value, 0.0): continue
                difference = ui.value - ri.value
                ui.value = different if difference > 0 else 0
                changed.append(ui)
            else:
                has_all_ingredients = False
        db.session.commit()

        if len(changed) == 0:
            responseObject = {
                'status': 'fail',
                'message': 'User has no ingredients in recipe'
            }

            return make_response(jsonify(responseObject), 400)

        responseObject = {
            'status': 'success',
            'has_all_ingredients': has_all_ingredients
        }

        return make_response(jsonify(responseObject), 200)


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
    Recipe details resource, given a Recipe ID query the database and gather
    all of the recipe fields. Return this result back to the user
    """
    def get(self, recipe_id):
        try:
            uuid.UUID(hex=recipe_id)
            recipe = Recipe.query.get(recipe_id)

            if recipe:
                responseObject = {
                    'status': 'success',
                    'data': recipe_to_json(recipe, make_json=False)
                }
                return make_response(jsonify(responseObject), 200)

            else:
                responseObject = {
                    'status': 'fail',
                    'message': 'Recipe %s not found.' % recipe_id
                }
                return make_response(jsonify(responseObject), 404)

        except ValueError:
            responseObject = {
                'status': 'fail',
                'message': '%s is not a valid recipe id.' % recipe_id
            }
            return make_response(jsonify(responseObject), 400)


recipe_api.add_resource(SearchResource, '/api/recipe/search')
recipe_api.add_resource(CreateResource, '/api/recipe')
recipe_api.add_resource(ModifyResource, '/api/recipe/<string:recipe_id>')
recipe_api.add_resource(DetailsResource, '/api/recipe/<string:recipe_id>')
recipe_api.add_resource(RateResource, '/api/recipe/<string:recipe_id>/rate')
recipe_api.add_resource(PrepareResource, '/api/recipe/<string:recipe_id>/prepare')
