import uuid
from api import app, db, bcrypt
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.postgresql import ARRAY
from flask_sqlalchemy import SQLAlchemy, BaseQuery
from sqlalchemy_searchable import SearchQueryMixin
from sqlalchemy_utils.types import TSVectorType
from sqlalchemy_searchable import make_searchable


class RecipeQuery(BaseQuery, SearchQueryMixin):
    pass

class Recipe(db.Model):
    """ Model for storing recipes """
    query_class = RecipeQuery
    __tablename__ = 'recipes'
    
    make_searchable()

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=lambda: uuid.uuid4().hex)
    name = db.Column(db.String(255), unique=True, nullable=False)
    description = db.Column(db.Text)
    steps = db.Column(ARRAY(db.Text))
    rating = db.Column(db.Float)
    num_ratings = db.Column(db.Integer, default=0)
    creator_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'))
    creator = db.relationship('User', back_populates='created_recipes')
    search_vector = db.Column(TSVectorType('name', 'description'))

    ingredients = association_proxy('recipe_ingredients', 'ingredient')

    def __init__(self, name, description=None, steps=None, rating=None, creator=None, creator_id=None):
        self.name = name
        self.description = description
        self.steps = steps
        self.rating = rating
        self.creator_id = creator_id
        self.creator = creator
