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

    # def post(self):
    #     post_data = request.get_json()

    #     ingredient = Ingredient.query.filter(Ingredient.name == post_data.get('ingredient_name')).first()
    #     user = User.query.filter(User.id = post_data.get('user_id'))
    #     pantry_ingredient = PantryIngredient.query.filter(
    #         (PantryIngredient.ingredient_id == indredient.id) | \
    #         (PantryIngredient.user_id == user.id)
    #     )
    #     if not ingredient:
    #         responseObject = {
    #             'status': 'fail',
    #             'message': 'Ingredient does not exist.',
    #         }
    #         return make_response(jsonify(responseObject), 202)

    #     if not user:
    #         responseObject = {
    #             'status': 'fail',
    #             'message': 'User does not exist.',
    #         }
    #         return make_response(jsonify(responseObject), 202)

    #     if not pantry_ingredient:

    #     try:
    #         pi = PantryIngredient(
    #             email=post_data.get('email'),
    #             username=post_data.get('username'),
    #             password=post_data.get('password')
    #         )
    #         # insert the user
    #         db.session.add(user)
    #         db.session.commit()
    #         # generate the auth token
    #         auth_token = user.encode_auth_token()
    #         responseObject = {
    #             'status': 'success',
    #             'message': 'Successfully registered.',
    #             'auth_token': auth_token.decode()
    #         }
    #         return make_response(jsonify(responseObject), 201)
    #     except Exception as e:
    #         responseObject = {
    #             'status': 'fail',
    #             'message': 'Some error occurred. Please try again.'
    #         }
    #         return make_response(jsonify(responseObject), 401)



    def delete(self):
        """ Remove an ingredient from the pantry """
        pass

    def patch(self):
        """ Change the amount of an ingredient in the pantry """

        # Check if user exists
        user = User.query.get(g.user_id)
        if not user:
            responseObject = {
                'status': 'fail',
                'message': 'User does not exist.'
            }
            return make_response(jsonify(responseObject), 202)

        patch_data = request.get_json()

        for entry in patch_data:

            # Check if ingredient exists
            ingredient = Ingredient.query.filter(Ingredient.name == entry['ingredient_name']).first()
            if not ingredient:
                responseObject = {
                    'status': 'fail',
                    'message': 'Ingredient does not exist.'
                }
                db.session.remove()
                return make_response(jsonify(responseObject), 202)

            pantry_ingredient = PantryIngredient(user = user, ingredient = ingredient, entry['value']).first()
            db.session.add(pantry_ingredient)

        db.session.commit()

        responseObject = {
            'status': 'success',
            'message': 'Ingredients added to pantry.',
            'auth_token': auth_token.decode()
        }
        return make_response(jsonify(responseObject), 201)




    def get(self):
        """ Get a list all of the ingredients, with the ones in the pantry marked """

        try:
            user = User.query.filter(User.id == g.user_id)
            if user:
                pantry_ingredients = PantryIngredient.query.filter(PantryIngredient.user_id == user.id).all()
                ingredientsObject = [{'name': i.pantry_ingredient.name, 'type': i.pantry_ingredient.measurement, 'value': i.value} for i in pantry_ingredients]

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

        except ValueError:
            responseObject = {
                'status': 'fail',
                'message': '%s is not a valid user id' % user_id
            }
            return make_response(jsonify(responseObject), 400)

# recipe_api.add_resource(DetailsResource, '/api/recipe/<string:recipe_id>')
pantry_api.add_resource(IngredientsResource, '/api/user/pantry/')
