from flask import jsonify

from api.models.user import User
from api.models.ingredient import PantryIngredient, RecipeIngredient, Ingredient, MeasurementEnum, CategoryEnum
from api.models.recipe import Recipe

from api import db

""" helper functions """

def ingredient_to_json(ingredient, make_json=True):
    obj = {
        'name': ingredient.name,
        'id': ingredient.id,
        'measurement': ingredient.measurement,
        'category': ingredient.category
    }

    if make_json:
        return jsonify(obj)

    return obj

def recipe_to_json(recipe, make_json=True, access_db=True, verbose=True):
    if access_db:
        ingredients = RecipeIngredient.query.filter(RecipeIngredient.recipe_id == recipe.id).all()
        ingredientsObject = [{'name': i.ingredient.name, 'measurement': i.ingredient.measurement.name, 'value': i.value} for i in ingredients]
        creator = recipe.creator.username if recipe.creator else ''
    else:
        ingredientsObject = []
        creator = ''

    if verbose:
        recipe_object = {
            'recipe_id': recipe.id,
            'name': recipe.name,
            'ingredients': ingredientsObject,
            'description': recipe.description,
            'steps': recipe.steps,
            'rating': recipe.rating,
            'creator': creator
        }
    else:
        recipe_object = {
            'recipe_id': recipe.id,
            'name': recipe.name,
            'description': recipe.description,
            'rating': recipe.rating
        }

    if make_json:
        return jsonify(recipe_object)

    return recipe_object

def user_to_json(user, make_json=True):
    pass

def json_to_ingredient(obj, access_db=False):
    name = obj['name']
    measurement = obj['measurement']
    if measurement not in [m.value for m in list(MeasurementEnum)]:
        # print(measurement)
        raise ValueError

    category = obj.get('category')

    if not category:
        category = 'MISC'
    elif category not in [c.value for c in list(CategoryEnum)]:
                # print(measurement)
        raise ValueError

    ingredient = None

    if access_db:
        ingredient = Ingredient.query.filter(Ingredient.name == name).first()

    if ingredient is None:
        ingredient = Ingredient(name=name, measurement=measurement, category=category)
        if access_db:
            db.session.add(ingredient)
    else:
        print('Ingredient %s already in db' % ingredient.name)

    return ingredient

def json_to_user(obj, access_db=False):
    email = obj['email']
    username = obj['username']
    password = obj['password']

    user = None

    if access_db:
        user = User.query.filter(User.username == username).first()
    if user is None:
        user = User(email=email, username=username, password=password)
    ingredients = obj['ingredients']

    for ing in ingredients:
        ingredient = Ingredient.query.filter(Ingredient.name == ing['name']).first()
        if ingredient is not None:
            if access_db:
                db.session.add(PantryIngredient(ingredient=ingredient, user=user, value=ing['value']))
            else:
                user.ingredients.append(ingredient)
    if access_db:
        db.session.add(user)
    return user

def json_to_recipe(obj, access_db=False, creator=None):
    name = obj['name']
    description = obj['description']
    steps = obj['steps']
    rating = obj.get('rating')

    recipe = None

    if access_db:
        recipe = Recipe.query.filter(Recipe.name == name).first()
    if recipe is None:
        recipe = Recipe(name=name, description=description, steps=steps, rating=rating)

    if creator:
        recipe.creator = creator
    ingredients = obj['ingredients']

    for ing in ingredients:
        ingredient = Ingredient.query.filter(Ingredient.name == ing['name']).first()
        if ingredient is not None:
            if access_db:
                db.session.add(RecipeIngredient(ingredient=ingredient, recipe=recipe, value=ing['value']))
            else:
                recipe.ingredients.append(ingredient)
    if access_db:
        db.session.add(recipe)
    return recipe
