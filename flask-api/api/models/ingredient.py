from enum import Enum
from api import app, db, bcrypt

class MeasurementEnum(Enum):
    MASS = 'mass'
    VOLUME = 'volume'
    COUNT = 'count'

class Ingredient(db.Model):
    """ Ingredient model for storing ingredients and their details """

    __tablename__ == 'ingredients'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    measurement = db.Column(db.Enum(MeasurementEnum), nullable=False)

    def __init__(self, name, measurement):
        self.name = name
        self.measurement = measurement
