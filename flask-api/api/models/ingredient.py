import uuid
from enum import Enum
from api import app, db, bcrypt
from api.models.user import User
from api.models.recipe import Recipe
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.associationproxy import association_proxy

class CategoryEnum(Enum):
    MEATS = 'MEATS'
    GRAINS = 'GRAINS'
    FRUITS = 'FRUITS'
    VEGETABLES = 'VEGETABLES'
    WET = 'WET'
    DRY = 'DRY'
    DAIRY = 'DAIRY'
    MISC = 'MISC'

class MeasurementEnum(Enum):
    MASS = 'MASS'
    VOLUME = 'VOLUME'
    COUNT = 'COUNT'

class Ingredient(db.Model):
    """ Ingredient model for storing ingredients and their details """

    __tablename__ = 'ingredients'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=lambda: uuid.uuid4().hex)
    name = db.Column(db.String(255), unique=True, nullable=False)
    measurement = db.Column(db.Enum(MeasurementEnum), nullable=False)
    category = db.Column(db.Enum(CategoryEnum), nullable=False)

    users = association_proxy('ingredient_users', 'user')
    recipes = association_proxy('ingredient_recipes', 'recipe')

    def __init__(self, name, measurement, category):
        self.name = name
        self.measurement = measurement
        self.category = category

    def __repr__(self):
        return '<Ingredient %s>' % self.name

class PantryIngredient(db.Model):

    __tablename__ = 'pantry_ingredients'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=lambda: uuid.uuid4().hex)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'))
    ingredient_id = db.Column(UUID(as_uuid=True), db.ForeignKey('ingredients.id'))
    value = db.Column(db.Float, nullable=False)

    user = db.relationship(User, backref='user_ingredients')
    ingredient = db.relationship(Ingredient, backref='ingredient_users')

    def __init__(self, ingredient=None, user=None, value=0):
        self.ingredient = ingredient
        self.user = user
        self.value = value

class RecipeIngredient(db.Model):

    __tablename__ = 'recipe_ingredients'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=lambda: uuid.uuid4().hex)
    recipe_id = db.Column(UUID(as_uuid=True), db.ForeignKey('recipes.id'))
    ingredient_id = db.Column(UUID(as_uuid=True), db.ForeignKey('ingredients.id'))
    value = db.Column(db.Float, nullable=False)

    recipe = db.relationship(Recipe, backref='recipe_ingredients')
    ingredient = db.relationship(Ingredient, backref='ingredient_recipes')

    def __init__(self, ingredient=None, recipe=None, value=0):
        self.ingredient = ingredient
        self.recipe = recipe
        self.value = value
