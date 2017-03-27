import uuid
from enum import Enum
from api import app, db, bcrypt
from api.models.user import User
from api.models.recipe import Recipe
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.associationproxy import association_proxy

class MeasurementEnum(Enum):
    MASS = 'mass'
    VOLUME = 'volume'
    COUNT = 'count'

class Ingredient(db.Model):
    """ Ingredient model for storing ingredients and their details """

    __tablename__ = 'ingredients'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=lambda: uuid.uuid4().hex)
    name = db.Column(db.String(255), unique=True, nullable=False)
    measurement = db.Column(db.Enum(MeasurementEnum), nullable=False)

    users = association_proxy('pantry_ingredients', 'user')
    recipes = association_proxy('recipe_ingredients', 'recipe')

    def __init__(self, name, measurement):
        self.name = name
        self.measurement = measurement

    def __repr__(self):
        return '<Ingredient %s>' % self.name

class PantryIngredient(db.Model):

    __tablename__ = 'pantry_ingredients'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=lambda: uuid.uuid4().hex)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'))
    ingredient_id = db.Column(UUID(as_uuid=True), db.ForeignKey('ingredients.id'))
    value = db.Column(db.Integer, nullable=False)

    user = db.relationship(User, backref='pantry_ingredients')
    ingredient = db.relationship(Ingredient, backref='pantry_ingredients')

    def __init__(self, value=0):
        self.set_value(value)

    def set_value(self, value):
        self.value = value

class RecipeIngredient(db.Model):

    __tablename__ = 'recipe_ingredients'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=lambda: uuid.uuid4().hex)
    recipe_id = db.Column(UUID(as_uuid=True), db.ForeignKey('recipes.id'))
    ingredient_id = db.Column(UUID(as_uuid=True), db.ForeignKey('ingredients.id'))
    value = db.Column(db.Integer, nullable=False)

    recipe = db.relationship(Recipe, backref='recipe_ingredients')
    ingredient = db.relationship(Ingredient, backref='recipe_ingredients')

    def __init__(self, value=0):
        self.set_value(value)

    def set_value(self, value):
        self.value = value
