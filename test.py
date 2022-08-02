import requests

poke = 'mew'
url = f'https://pokeapi.co/api/v2/pokemon/{poke}'
response = requests.get(url)
if not response.ok:
    print('error')

pokemon = response.json()
this_poke = {
    "Ability":pokemon["abilities"][0]['ability']['name'],
    "Base Exp":pokemon["base_experience"],
    "Base Attk":pokemon["stats"][1]['base_stat'],
    "Base HP":pokemon["stats"][0]['base_stat'],
    "Base Def":pokemon["stats"][2]['base_stat'],
    "Sprite":pokemon["sprites"]['other']['official-artwork']["front_default"]
}
print(this_poke)

{# <form action="{{url_for('finder')" method="POST">
    {{form.hidden_tag}}
    <div class="mb-3">
        {{form.poke_name.label(class="form-label")}}
        {{form.poke_name(class="form-control")}}
        {% for error in form.poke_name.errors%}
            <small style="color:red">{{error}}</small>
        {% endfor %}
    </div>
    <div>
        {{form.submit(class="btn btn-primary")}}<br>
         <small style="color:red">{{error}}</small>
    </div>
</form> #}