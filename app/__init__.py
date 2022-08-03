from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

login = LoginManager(app)

login.login_view = 'login'

#builting login function that displays message when trying to enter fields that require login
login.login_message = 'Ye shall not pass until doth logith inith'
login.login_message_category = 'danger'


from app import routes, models