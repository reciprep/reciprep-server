from flask import jsonify

from api.models.user import User
from api.models.ingredient import PantryIngredient, RecipeIngredient, Ingredient, MeasurementEnum
from api.models.recipe import Recipe

from api import db

""" helper functions """

def ingredient_to_json(ingredient, make_json=True):
    obj = {
        'name': ingredient.name,
        'id': ingredient.id,
        'measurement': ingredient.measurement
    }

    if make_json:
        return jsonify(obj)
    else:
        return obj

def recipe_to_json(recipe, make_json=True, access_db=True):

    for i in recipe.ingredients:
        print(i.value)

def user_to_json(user, make_json=True):
    pass

def json_to_ingredient(obj, access_db=False):
    name = obj['name']
    measurement = obj['measurement']
    if measurement not in [m.value for m in list(MeasurementEnum)]:
        print(measurement)
        raise ValueError

    ingredient = None

    if access_db:
        ingredient = Ingredient.query.filter(Ingredient.name == name).first()

    if ingredient is None:
        ingredient = Ingredient(name=name, measurement=measurement)
        if access_db:
            db.session.add(ingredient)
    else:
        print('Ingredient %s already in db' % ingredient.name)

    return Ingredient(name=name, measurement=measurement)

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

def json_to_recipe(obj, access_db=False):
    name = obj['name']
    description = obj['description']
    steps = obj['steps']
    rating = obj['rating']

    recipe = None

    if access_db:
        recipe = Recipe.query.filter(Recipe.name == name).first()
    if recipe is None:
        recipe = Recipe(name=name, description=description, steps=steps, rating=rating)

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
