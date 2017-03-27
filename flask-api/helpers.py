import json
from api.models.user import User
from api.models.ingredient import Ingredient, MeasurementEnum
from api.models.recipe import Recipe

from api import db

""" helper functions """

def json_to_ingredient(obj):
    name = obj['name']
    measurement = obj['measurement']
    if measurement not in MeasurementEnum:
        raise ValueError
    return Ingredient(name=name, measurement=measurement)

def json_to_user(obj, check_db=False):
    email = obj['email']
    username = obj['username']
    password = obj['password']

    user = User(email=email, username=username, password=password)

    if check_db:
        ingredients = obj['ingredients']

        for ingr_name in ingredients:
            ingredient = Ingredient.query.filter(Ingredient.name == ingr_name).first()
            if ingredient is not None:
                user.ingredients.append(ingredient)

    return user

def json_to_recipe(obj, check_db=False):
    name = obj['name']
    descrption = obj['description']
    steps = obj['steps']
    rating = obj['rating']

    recipe = Recipe(name=name, description=description, steps=steps, rating=rating)

    if check_db:
        ingredients = obj['ingredients']

        for ingr_name in ingredients:
            ingredient = Ingredient.query.filter(Ingredient.name == ingr_name).first()
            if ingredient is not None:
                recipe.ingredients.append(ingredient)

    return recipe
