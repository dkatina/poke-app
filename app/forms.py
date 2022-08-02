from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from app import app



class PokeForm(FlaskForm):
    poke_name = StringField('Pokemon Name', validators=[DataRequired()])
    submit = SubmitField('Find Pokemon')

