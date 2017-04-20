import uuid

from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.postgresql import ARRAY

from api import app, db, bcrypt
from api.models.user import User
from api.models.recipe import Recipe

class Rating(db.Model):
    __tablename__ = 'ratings'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=lambda: uuid.uuid4().hex)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'))
    recipe_id = db.Column(UUID(as_uuid=True), db.ForeignKey('recipes.id'))
    value = db.Column(db.Float, nullable=False)

    user = db.relationship(User, backref='user_ratings')
    recipe = db.relationship(Recipe, backref='rating_users')

    def __init__(self, user=None, recipe=None, value=0):
        self.user = user
        self.recipe = recipe
        self.value = value
