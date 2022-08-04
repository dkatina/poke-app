from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, RadioField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from app.models import User
from jinja2.utils import markupsafe



class PokeForm(FlaskForm):
    poke_name = StringField('Pokemon Name', validators=[DataRequired()])
    submit = SubmitField('Find Pokemon')
