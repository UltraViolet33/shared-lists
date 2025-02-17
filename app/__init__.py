from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask import Flask
import os

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=[],  # No global limits, only for specific routes
    storage_uri="memory://",
)


def create_app(config_type=None):
    app = Flask(__name__)

    if config_type == None:
        config_type = os.getenv("CONFIG_TYPE", default="config.DevelopmentConfig")

    app.config.from_object(config_type)

    initialize_extensions(app)
    register_blueprints(app)

    return app


def initialize_extensions(app):
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    limiter.init_app(app)

    from app.models.User import User
    from app.models.List import List

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.filter(User.id == int(user_id)).first()

    login_manager.login_view = "auth.login"


def register_blueprints(app):
    from .auth import auth
    from .tasks import tasks
    from .lists import lists
    from .commands import commands

    app.register_blueprint(auth, url_prefix="/")
    app.register_blueprint(lists, url_prefix="/")
    app.register_blueprint(tasks, url_prefix="/tasks")
    app.register_blueprint(commands)
