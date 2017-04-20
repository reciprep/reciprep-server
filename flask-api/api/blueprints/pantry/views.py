from flask import Blueprint, request, make_response, jsonify, g
from flask.views import MethodView
from flask_restful import Api, Resource, url_for

from api import bcrypt, db
from api.models.user import User
from api.models.ingredient import Ingredient, PantryIngredient
from api.decorators import is_logged_in

pantry_blueprint = Blueprint('pantry', __name__)
pantry_api = Api(pantry_blueprint)

class IngredientsResource(Resource):
    """
    Resources for managing ingredients in the User's pantry
    """
    decorators = [is_logged_in]


    def patch(self):
        """ 
        Change the amount of an ingredient in the pantry 
        Works for existing ingredients or new ingredients
        Checks for valid User and Ingredients
            - returns status 'fail' otherwise
            - does not change database if there is a failure for the user or any of the ingredients
        Reads JSON from HTTP request, contiaining info about the ingredients to be changed
        Commits changes to the database using SQL-Alchemy
        """
        try:
            user = User.query.get(g.user_id)
            if not user:
                responseObject = {
                    'status': 'fail',
                    'message': 'User does not exist.'
                }
                return make_response(jsonify(responseObject), 202)

            patch_data = request.get_json()

            for entry in patch_data.get("ingredients"):

                ingredient = Ingredient.query.filter(Ingredient.name == entry.get('ingredient_name')).first()

                if not ingredient:
                    responseObject = {
                        'status': 'fail',
                        'message': 'Ingredient does not exist.'
                    }
                    db.session.remove()
                    return make_response(jsonify(responseObject), 202)

                p_i = PantryIngredient.query.filter( (PantryIngredient.user_id == g.user_id) & (PantryIngredient.ingredient_id == ingredient.id) ).first()
                
                if p_i:
                    p_i.value = entry['value']
                else:
                    pantry_ingredient = PantryIngredient(user = user, ingredient = ingredient, value=entry['value'])
                    db.session.add(pantry_ingredient)

            db.session.commit()
            responseObject = {
                'status': 'success',
                'message': 'Ingredients added to pantry.'
            }

            return make_response(jsonify(responseObject), 201)



        except Exception as e:
            print(e)



    def get(self):
        """ 
        Get a list all of the ingredients
        """

        try:
            user = User.query.filter(User.id == g.user_id)
            if user:
                pantry_ingredients = PantryIngredient.query.filter(PantryIngredient.user_id == g.user_id).all()
                ingredientsObject = []
                for i in pantry_ingredients:
                    ingredient = Ingredient.query.filter(Ingredient.id == i.ingredient_id).first()
                    ingredientsObject.append({'name': ingredient.name, 'type': ingredient.measurement.value, 'value': i.value, "category": ingredient.category.value}) 

                responseObject = {
                    'status': 'success',
                    'data': {
                        'ingredients': ingredientsObject
                    }
                }
                return make_response(jsonify(responseObject), 200)

            else:
                responseObject = {
                    'status': 'fail',
                    'message': 'User %s not found' % user_id
                }
                return make_response(jsonify(responseObject), 404)

        except Exception as e:
            print(e)
            responseObject = {
                'status': 'fail',
                'message': '%s is not a valid user id' % user_id
            }
            return make_response(jsonify(responseObject), 400)

# recipe_api.add_resource(DetailsResource, '/api/recipe/<string:recipe_id>')
pantry_api.add_resource(IngredientsResource, '/api/user/pantry')
