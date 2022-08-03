from flask import render_template, request, url_for, flash, redirect
import requests
from app import app
from .forms import *
from .models import User
from flask_login import login_user, login_required, logout_user, current_user

@app.route('/')
def index():
    return render_template('index.html.j2')

@app.route('/finder', methods=['GET', 'POST'])
def finder():
    form = PokeForm()
    if request.method == 'POST':
        poke_name = form.poke_name.data.lower()

        url = f'https://pokeapi.co/api/v2/pokemon/{poke_name}'
        response = requests.get(url)
        if not response.ok:
            error_string = 'An Error has Occured while trying to preform this search'
            return render_template('finder.html.j2', error=error_string, form=form)
        
        pokemon = response.json()
        this_poke = {
            "Ability":pokemon["abilities"][0]['ability']['name'],
            "BaseExp":pokemon["base_experience"],
            "BaseAttk":pokemon["stats"][1]['base_stat'],
            "BaseHP":pokemon["stats"][0]['base_stat'],
            "BaseDef":pokemon["stats"][2]['base_stat'],
            "Sprite":pokemon["sprites"]['other']['official-artwork']["front_default"]
        }
        return render_template('finder.html.j2', poke=this_poke, name=poke_name.title(), form=form)
    
    return render_template('finder.html.j2', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'POST' and form.validate_on_submit():
        try:
            new_user = {
                "first_name": form.first_name.data.title(),
                "last_name": form.first_name.data.title(),
                "email": form.email.data.lower(),
                "password": form.password.data,
                "icon": form.icon.data
            }
            #Creates empty user
            new_user_obj = User()
            #Uses our function to unpack the user dictionary into the user clas
            new_user_obj.from_dict(new_user)
            #saves the user to database
            new_user_obj.save()
        except:
            flash("Unexpected error has occured", "danger")
            return render_template('register.html.j2', form=form)
        flash("Successfully registered", "success")
        return redirect(url_for('login'))
    
    return render_template('register.html.j2', form=form)

@app.route('/edit_user', methods=['GET', 'POST'])
def edit_user():
    form = EditProfileForm()
    if request.method == 'POST' and form.validate_on_submit():
        edited_user = {
            "first_name": form.first_name.data.title(),
            "last_name": form.first_name.data.title(),
            "email": form.email.data.lower(),
            "password": form.password.data,
            "icon": form.icon.data if int(form.icon.data) != 9000 else current_user.icon
        }
        user = User.query.filter_by(email=edited_user['email']).first()
        if user and user.email != current_user.email:
            flash("Silly Goose that's not your email!", 'danger')
            return redirect('edit_user')
        try:
            current_user.from_dict(edited_user)
            current_user.save()
            flash("Profile Updated, Maybe next time don't Screw-up during registration", "info")
        except:
            flash("Unexpected Error occured", 'danger')
            return redirect(url_for('edit_user'))
        return redirect(url_for('index'))
    return render_template('register.html.j2',form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data.lower()
        password = form.password.data

        user = User.query.filter_by(email=email).first()
        if user and user.check_pass(password):
            flash('Welcome', 'success')
            login_user(user)
            return redirect(url_for('index'))
        flash('Incorrect Email or Password', 'danger')
        return render_template('login.html.j2', form=form)
    return render_template('login.html.j2' , form=form)

@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    flash('See ya Later Alligator', 'info')
    return redirect(url_for('index'))





