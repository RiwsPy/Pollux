from json import load
from json.decoder import JSONDecodeError
import os
from pathlib import Path
from . import app
from flask import render_template, jsonify, request
from api_ext.clips import Clips
from api_ext import BadStatusError

BASE_DIR = Path(__file__).resolve().parent.parent


# TODO: A BOUGER !
DESC1 = """
Tuto ?

Sur cette carte vous êtes invités à créer votre propre zone de recherche.
Une fois fait, Pollux identifie les différents éléments présents dans cette zone.
Dans le panneau de droite, s'affichera des recommandations d'éclairage en fonction de ceux-ci.

En passant votre souris sur la forme créée, s'affichera le nombre des différents éléments trouvés.
"""

DESC2 = """
Pleins de trucs ici, trop faciles à lire.
"""

DESC3 = """
Des choses encore mieux là.
"""

MAP_NB_TO_DATA = {
    "1": {
        "lines": DESC1.split('\n'),
        "button_url": '/map/1',
        "template_name_or_list": 'maps.html',
        'script_filename': 'js/leafmap.js'},
    "2": {
        "lines": DESC2.split('\n'),
        "button_url": '/map/2',
        "template_name_or_list": 'heatmaps.html',
        'script_filename': 'js/conflictTreeCrossing.js'},
    "3": {
        "lines": DESC3.split('\n'),
        "button_url": '/map/3',
        "template_name_or_list": 'heatmaps.html',
        'script_filename': 'js/conflictTreeLum.js'}
}


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/map/<map_nb>')
def show_map(map_nb):
    return render_template(**MAP_NB_TO_DATA.get(map_nb, {}))


@app.route('/api/<filename>', methods=['GET'])
def print_json(filename):
    no_way_files = ()
    if filename in no_way_files:
        return jsonify({'Error': f'FileNotFoundError: {filename} not found'})

    try:
        with open(os.path.join(BASE_DIR, 'db/' + filename), 'r') as file:
            return jsonify(load(file))
    except FileNotFoundError:
        return jsonify({'Error': f'FileNotFoundError: {filename} not found'})
    except JSONDecodeError:
        return jsonify({'Error': f'JSONDecodeError: {filename} : format incorrect.'})


@app.route('/clips/', methods=['POST'])
def clips_recommendation():
    cl = Clips()
    try:
        req = cl.call(url="", data=request.data)
    except BadStatusError:
        return jsonify({"recommendation": "Erreur"})

    return jsonify(req)


@app.route('/mentions_legales/', methods=['GET'])
def mentions_legales():
    return render_template('mentions_legales.html')


@app.route('/encyclopedia/', methods=['GET'])
def encyclopedia():
    return render_template('encyclopedia.html')


@app.route('/map_desc/<map_nb>', methods=['GET'])
def show_map_description(map_nb):
    return render_template('map_desc.html',
                           button_txt='Accéder à la carte',
                           lines=MAP_NB_TO_DATA[map_nb]['lines'],
                           button_url=MAP_NB_TO_DATA[map_nb]['button_url'])
