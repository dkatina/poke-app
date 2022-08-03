from email import message
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, RadioField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from app import app
from .models import User
import random
from jinja2.utils import markupsafe



class PokeForm(FlaskForm):
    poke_name = StringField('Pokemon Name', validators=[DataRequired()])
    submit = SubmitField('Find Pokemon')

class LoginForm(FlaskForm):
#  variable Field Type   Lable             Validators
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', 
        validators=[DataRequired(), EqualTo('password', message='Password Must Match')])
    submit = SubmitField('Register')

    r1=random.randint(1,1000)
    r2=random.randint(1001,2000)
    r3=random.randint(2001,3000)
    r4=random.randint(3001,4000)

    #https://avatars.dicebear.com/api/big-smile/

    r1_img = markupsafe.Markup(f'<img src="https://avatars.dicebear.com/api/big-smile/{r1}.svg" height="75px">')
    r2_img = markupsafe.Markup(f'<img src="https://avatars.dicebear.com/api/big-smile/{r2}.svg" height="75px">')
    r3_img = markupsafe.Markup(f'<img src="https://avatars.dicebear.com/api/big-smile/{r3}.svg" height="75px">')
    r4_img = markupsafe.Markup(f'<img src="https://avatars.dicebear.com/api/big-smile/{r4}.svg" height="75px">')

    icon = RadioField('Avatar', validators=[DataRequired()], choices=[(r1,r1_img),(r2, r2_img),(r3, r3_img),(r4, r4_img)])

    def validate_email(form, field):
        user_with_email = User.query.filter_by(email=field.data).first()
        if user_with_email:
            return ValidationError('Account already registered under this email address')

class LoginForm(FlaskForm):
#  variable Field Type   Lable             Validators
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')



class EditProfileForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', 
        validators=[DataRequired(), EqualTo('password', message='Password Must Match')])
    submit = SubmitField('Update')

    r1=random.randint(1,1000)
    r2=random.randint(1001,2000)
    r3=random.randint(2001,3000)
    r4=random.randint(3001,4000)

    r1_img = markupsafe.Markup(f'<img src="https://avatars.dicebear.com/api/big-smile/{r1}.svg" height="75px">')
    r2_img = markupsafe.Markup(f'<img src="https://avatars.dicebear.com/api/big-smile/{r2}.svg" height="75px">')
    r3_img = markupsafe.Markup(f'<img src="https://avatars.dicebear.com/api/big-smile/{r3}.svg" height="75px">')
    r4_img = markupsafe.Markup(f'<img src="https://avatars.dicebear.com/api/big-smile/{r4}.svg" height="75px">')

    icon = RadioField('Avatar', validators=[DataRequired()], choices=[(r1,r1_img),(r2, r2_img),(r3, r3_img),(r4, r4_img)])