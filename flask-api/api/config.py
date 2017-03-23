import os
basedir = os.path.abspath(os.path.dirname(__file__))
postgres_local_base = 'postgresql://postgres:@localhost/'
database_name = 'reciprep_db'


class BaseConfig:
    """Base configuration."""
    SECRET_KEY = os.getenv('SECRET_KEY', 'koulopoulos')
    DEBUG = False
    BCRYPT_LOG_ROUNDS = 13
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_EXPIRATION_DAYS = 0
    JWT_EXPIRATION_SECONDS = 60


class DevelopmentConfig(BaseConfig):
    """Development configuration."""
    DEBUG = True
    BCRYPT_LOG_ROUNDS = 4
    SQLALCHEMY_DATABASE_URI = postgres_local_base + database_name

class TestingConfig(BaseConfig):
    """Testing configuration."""
    DEBUG = True
    TESTING = True
    BCRYPT_LOG_ROUNDS = 4
    SQLALCHEMY_DATABASE_URI = postgres_local_base + database_name + '_test'
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    LIVESERVER_PORT = 80


# class ProductionConfig(BaseConfig):
#     """Production configuration."""
#     SECRET_KEY = 'koulopoulos'
#     DEBUG = False
#     SQLALCHEMY_DATABASE_URI = 'postgresql:///example'
#     JWT_EXPIRATION_DAYS = 7
#     JWT_EXPIRATION_SECONDS = 0
