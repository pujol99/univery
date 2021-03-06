from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_admin.contrib.sqla import ModelView
from app.config import Config
from .main.utils import *

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
MAINTENANCE = False

def create_app(config_class=Config):
    app = Flask(__name__)
    app.before_request(MaintenanceModeHandler(MAINTENANCE))
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    from app.users.routes import users
    from app.main.routes import main
    from app.errors.handlers import errors
    from app.subjects.routes import subjects
    from app.deliveries.routes import deliveries
    app.register_blueprint(users)
    app.register_blueprint(main)
    app.register_blueprint(errors)
    app.register_blueprint(subjects)
    app.register_blueprint(deliveries)

    return app