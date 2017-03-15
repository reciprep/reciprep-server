import os

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app_settings = os.getenv(
    'APP_SETTINGS',
    'api.config.DevelopmentConfig'
)
app.config.from_object(app_settings)

bcrypt = Bcrypt(app)
db = SQLAlchemy(app)

from api.endpoints.auth.views import auth_blueprint
app.register_blueprint(auth_blueprint)
