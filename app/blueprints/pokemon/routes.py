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
            "Sprite":pokemon["sprites"]['other']['official-artwork']["front_default"]
        }
        if current_user.is_authenticated:
            return render_template('finder.html.j2', poke=this_poke, name=poke_name.title(), space_in_team=current_user.check_team() ,form=form)
        else:
            return render_template('finder.html.j2', poke=this_poke, name=poke_name.title(),form=form)
    return render_template('finder.html.j2', form=form)

@pokemon.route('/catch_pokemon/<poke_name>', methods=['GET', 'POST'])
@login_required
def catch_pokemon(poke_name):
    poke = Pokemon.query.get(poke_name)
    if not poke:
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
            "Sprite":pokemon["sprites"]['other']['official-artwork']["front_default"]
        }
        this_poke = Pokemon()
        this_poke.from_dict(poke_dict)
        this_poke.save()
        current_user.catch_poke(this_poke)
        flash("Pokemon Successfully caught!", "success")
        return redirect(url_for('pokemon.finder'))

    # poke_in_team = (True if Pokemon.query.filter_by(user_id=current_user.id, name=poke_dict['Name']).first() else False)
    if current_user.in_my_team(poke):
        flash("You already have this Pokemon!", "warning")
        return redirect(url_for('pokemon.finder'))
    elif not current_user.check_team:
        flash("You're team is already full!", "warning")
        return redirect(url_for('pokemon.finder'))
    else:
        current_user.catch_poke(poke)
        flash("Pokemon Successfully caught!", "success")
        return redirect(url_for('pokemon.finder'))

@pokemon.route('/my_team')
@login_required
def my_team():
    return render_template('my_team.html.j2', pokemon=current_user.pokemon.all())

@pokemon.route('/release_pokemon/<name>')
@login_required
def release_pokemon(name):
    poke = Pokemon.query.get(name)
    print(poke)
    if not poke:
        flash("User hurt themselves in confusion, they probably shouldn't try that aggain", 'danger')
        return redirect(url_for('pokemon.index'))
    current_user.release(poke)
    flash(f"You have returned {name} to the wild!", "success")
    return redirect(url_for('pokemon.my_team'))



@pokemon.route('/browse_trainers')
@login_required
def browse_trainers():
    return render_template('browse_trainers.html.j2', trainers=User.query.filter(User.id!=current_user.id).all(), me=User.query.get(current_user.id))

@pokemon.route('/battle/<id>')
@login_required
def battle(id):
    return render_template('battle.html.j2', me=User.query.get(current_user.id), trainer=User.query.get(id))

@pokemon.route('/results/<id>')
@login_required
def results(id):
    trainer = User.query.get(id)
    hp1= 0
    df1= 0
    attk1= 0
    hp2=0
    df2=0
    attk2=0
    for pokemon in current_user.pokemon:
        hp1+= int(pokemon.hp)
        df1 += int(pokemon.defense)/100
        attk1+= int(pokemon.attk)
    for pokemon in trainer.pokemon:
        hp2+= int(pokemon.hp)
        df2 += int(pokemon.defense)/100
        attk2+= int(pokemon.attk)
    hp1 *= df1
    hp2 *= df2
    hp1/=attk2
    hp2/=attk1
    if hp1 >= hp2:
        current_user.wins += 1
        trainer.loses += 1
        current_user.save()
        trainer.save()
        return render_template('results.html.j2', winner=current_user)
    else:
        current_user.loses += 1
        trainer.wins += 1
        current_user.save()
        trainer.save()
        return render_template('results.html.j2', winner=trainer)

@pokemon.route('/this_trainer/<id>')
@login_required
def this_trainer(id):
    trainer = User.query.get(id)
    return render_template('this_trainer.html.j2', pokemon=trainer.pokemon.all(), trainer=trainer)