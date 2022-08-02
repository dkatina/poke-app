from flask import Flask, render_template, request
import requests
from app import app
from .forms import *

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

        