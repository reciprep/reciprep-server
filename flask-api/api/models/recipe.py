from api import app, db, bcrypt
from sqlalchemy.dialects.postgresql import UUID

class Recipe(db.Model):
    """ Model for storing recipes """

    __tablename__ = 'recipes'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)

    def __init__(self):
        pass
