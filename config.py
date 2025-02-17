import os
from dotenv import load_dotenv

project_folder = os.path.expanduser("")
load_dotenv(os.path.join(project_folder, ".env"))

BASEDIR = os.path.abspath(os.path.dirname(__file__))

DATABASE_URL = os.getenv("DATABASE_URL")

class Config(object):
    FLASK_ENV = "development"
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.getenv("SECRET_KEY", default="BAD_SECRET_KEY")

    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    FLASK_ENV = "production"


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(object):
    TESTING = True
    SECRET_KEY = os.getenv("SECRET_KEY", default="BAD_SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = (
        f"sqlite:///{os.path.join(BASEDIR, 'instance', 'test.db')}"
    )
