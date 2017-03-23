import uuid
from api import app, db, bcrypt
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.postgresql import ARRAY

class Recipe(db.Model):
    """ Model for storing recipes """

    __tablename__ = 'recipes'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=lambda: uuid.uuid4().hex)
    name = db.Column(db.String(255), unique=True, nullable=False)
    description = db.Column(db.Text)
    steps = db.Column(ARRAY(db.Text))
    rating = db.Column(db.Float)
    num_ratings = db.Column(db.Integer, default=0)

    ingredients = association_proxy('recipe_ingredients', 'ingredient')

    def __init__(self, name, description=None, steps=None, rating=None):
        self.name = name
        self.description = description
        self.steps = steps
        self.rating = rating
