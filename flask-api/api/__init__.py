import os

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_searchable import make_searchable

app = Flask(__name__)

app_settings = os.getenv(
    'APP_SETTINGS',
    'api.config.DevelopmentConfig'
)
app.config.from_object(app_settings)

bcrypt = Bcrypt(app)
db = SQLAlchemy(app)

from api.blueprints.auth.views import auth_blueprint
from api.blueprints.recipe.views import recipe_blueprint
from api.blueprints.pantry.views import pantry_blueprint
app.register_blueprint(auth_blueprint)
app.register_blueprint(recipe_blueprint)
app.register_blueprint(pantry_blueprint)
