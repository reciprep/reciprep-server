from api import app, db, bcrypt


class UserIngredient(db.Model):
    """ Model for storing ingredients in every user's pantry """

    __tablename__ == 'user_ingredients'

    

    def __init__(self):
        pass
