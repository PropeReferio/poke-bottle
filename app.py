from flask import Flask, render_template, request
import requests
import os
# import settings

# print(settings.favorite_poke)

app = Flask(__name__)

def get_poke_json(name):
	return requests.get(f"https://pokeapi.co/api/v2/pokemon/{name}", verify=False)

def get_poke_type_1(name):
	return get_poke_json(name).json()['types'][0]['type']['name'].capitalize()

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/poke', methods=['POST'])
def poke():
	name = request.form['poke'].lower()
	r = get_poke_json(name).json()
	name = r['name'].capitalize()
	number = r['id']
	type1 = r['types'][0]['type']['name'].capitalize()
	type2 = ''
	if len(r['types']) == 2:
		type2 = r['types'][1]['type']['name'].capitalize()
	return render_template('poke.html', name=name, number=number, type1=type1, type2=type2)

if __name__ == '__main__':
	app.run(debug=True)
