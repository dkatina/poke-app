from multiprocessing.context import SpawnContext
from flask import render_template, request, url_for, flash, redirect
import requests
from .forms import *
from app.models import User, Pokemon
from flask_login import login_user, login_required, logout_user, current_user
from . import bp as pokemon

@pokemon.route('/')
def index():
    return render_template('index.html.j2')

@pokemon.route('/finder', methods=['GET', 'POST'])
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
            "Name": poke_name.title(),
            "Ability":pokemon["abilities"][0]['ability']['name'],
            "BaseExp":pokemon["base_experience"],
            "BaseAttk":pokemon["stats"][1]['base_stat'],
            "BaseHP":pokemon["stats"][0]['base_stat'],
            "BaseDef":pokemon["stats"][2]['base_stat'],
            "Sprite":pokemon["sprites"]['other']['official-artwork']["front_default"],
            "User_id": current_user.id
        }
        
        print(current_user.pokemon.all())
        return render_template('finder.html.j2', poke=this_poke, name=poke_name.title(), space_in_team=len(current_user.pokemon.all()) < 6,form=form)
    
    return render_template('finder.html.j2', form=form)

@pokemon.route('/catch_pokemon/<poke_name>', methods=['GET', 'POST'])
@login_required
def catch_pokemon(poke_name):
    url = f'https://pokeapi.co/api/v2/pokemon/{poke_name.lower()}'
    response = requests.get(url)
    pokemon = response.json()
    poke_dict = {
        "Name": poke_name.title(),
        "Ability":pokemon["abilities"][0]['ability']['name'],
        "BaseExp":pokemon["base_experience"],
        "BaseAttk":pokemon["stats"][1]['base_stat'],
        "BaseHP":pokemon["stats"][0]['base_stat'],
        "BaseDef":pokemon["stats"][2]['base_stat'],
        "Sprite":pokemon["sprites"]['other']['official-artwork']["front_default"],
        "User_id": current_user.id
    }
    poke_in_team = (True if Pokemon.query.filter_by(user_id=current_user.id, name=poke_dict['Name']).first() else False)
    if poke_in_team:
        flash("You already have this Pokemon!", "warning")
        return redirect(url_for('pokemon.finder'))
    elif len(current_user.pokemon.all()) >= 6:
        flash("You're team is already full!", "warning")
        return redirect(url_for('pokemon.finder'))
    else:
        this_poke = Pokemon()
        this_poke.from_dict(poke_dict)
        this_poke.save()
        flash("Pokemon Successfully caught!", "success")
        return redirect(url_for('pokemon.finder'))

@pokemon.route('/my_team')
@login_required
def my_team():
    return render_template('my_team.html.j2', pokemon=current_user.pokemon.all())

@pokemon.route('/release_pokemon/<int:id>')
def release_pokemon(id):
    poke = Pokemon.query.get(id)
    if poke and poke.master.id != current_user.id:
        flash("User hurt themselves in confusion, they probably shouldn't try that aggain", 'danger')
        return redirect(url_for('pokemon.index'))
    name = poke.name
    poke.release()
    flash(f"You have returned {name} to the wild!", "success")
    return redirect(url_for('pokemon.my_team'))


