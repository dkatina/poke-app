from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_migrate import Migrate
from flask_login import LoginManager



db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()



def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)

    login.login_view = 'auth.login'
    #builting login function that displays message when trying to enter fields that require login
    login.login_message = 'Ye shall not pass until doth logith inith'
    login.login_message_category = 'danger'

    from.blueprints.auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    from.blueprints.pokemon import bp as pokemon_bp
    app.register_blueprint(pokemon_bp)

    return app



from app import models