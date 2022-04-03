from json import load
from json.decoder import JSONDecodeError
import os
from pathlib import Path
from . import app
from flask import render_template, jsonify, request
from api_ext.clips import Clips
from api_ext import BadStatusError
from .map_desc import DESC1, DESC2, DESC3

BASE_DIR = Path(__file__).resolve().parent.parent

MAP_NB_TO_DATA = {
    "1": {
        "lines": DESC1.split('\n'),
        "template_name_or_list": 'maps.html',
        'script_filename': 'js/leafmap.js',
        'title': 'Carte des recommandations',
        'accroche': "Un outil permettant d'identifier dans une zone précise, les éléments impactant l'éclairage public et d'indiquer leurs recommandations.",
        'icon': 'button_recommandation.png',
        'href': '/map/1',
        'href_desc': '/map_desc/1'},
    "2": {
        "lines": DESC2.split('\n'),
        "template_name_or_list": 'heatmaps.html',
        'script_filename': 'js/conflictTreeCrossing.js',
        'title': 'Carte de contradiction',
        'accroche': "Un outil mettant en lumière les zones exigeant un éclairage contradictoire en fonction de l'avancée de la nuit.",
        'icon': 'button_contradiction.png',
        'href': '/map/2',
        'href_desc': '/map_desc/2'},
    "3": {
        "lines": DESC3.split('\n'),
        "template_name_or_list": 'heatmaps.html',
        'script_filename': 'js/conflictTreeLum.js',
        'title': "Carte d'impact",
        'accroche': "Un outil pour identifier les luminaires ayant un impact fort sur la biodiversité à proximité.",
        'icon': 'button_impact.png',
        'href': '/map/3',
        'href_desc': '/map_desc/3'},
    "encyclopédie": {
        "lines": '',
        'title': "Encyclopédie",
        'accroche': "Un outil pour éclairer les lanternes.",
        'icon': 'button_encyclopedie.png',
        'href': '/encyclopedia',
        'href_desc': '/encyclopedia'}
}

DICT_DATA = {
    'columns': ['Nom', 'Origine', 'Licence', 'Détails'],
    'lines': [
        {'name': "Arbres de Grenoble",
         'href': 'https://data.metropolegrenoble.fr/ckan/dataset/les-arbres-de-grenoble/resource/f09de972-1a29-491d-8c34-b80edda0e5ff',
         'href_txt': 'Data Métropole',
         'licence': 'ODbL',
         'details': 'Mise à jour du 10 Janvier 2017'
         },
        {'name': "Luminaires de Grenoble",
         'href': 'https://data.metropolegrenoble.fr/',
         'href_txt': 'Data Métropole',
         'upDate': '/',
         'licence': 'ODbL',
         'details': 'Données non disponibles'
         },
        {'name': "Passages piétons",
         'href': 'https://overpass-turbo.eu/',
         'href_txt': 'OpenStreetMap',
         'licence': 'ODbL',
         'details': '/'
         },
        {'name': "Parcs",
         'href': 'https://overpass-turbo.eu/',
         'href_txt': 'OpenStreetMap',
         'licence': 'ODbL',
         'details': '/'
         },
        {'name': "Bâtiments ouverts au public",
         'href': 'https://overpass-turbo.eu/',
         'href_txt': 'OpenStreetMap',
         'licence': 'ODbL',
         'details': '/'
         },
        {'name': "Arrêts & voies de bus",
         'href': 'https://data.mobilites-m.fr/',
         'href_txt': 'SMMAG',
         'licence': 'ODbL',
         'details': 'Mise à jour du 25 janvier 2022'
         },
        {'name': 'Accidents de voiture',
         'href': 'https://www.data.gouv.fr/fr/datasets/bases-de-donnees-annuelles-des-accidents-corporels-de-la-circulation-routiere-annees-de-2005-a-2020/?reuses_page=2#community-reuses',
         'href_txt': 'data.gouv.fr',
         'licence': 'ODbL',
         'details': 'Mise à jour du 26 Novembre 2021'
         },
        {'name': "Observations d'oiseaux",
         'href': 'https://openobs.mnhn.fr/',
         'href_txt': 'INPN OpenObs',
         'licence': 'Etalab',
         'details': 'Mise à jour du 2 Février 2022'
         },
        {'name': "Artères principales de Grenoble",
         'href': '#',
         'href_txt': '/',
         'licence': 'ODbL',
         'details': 'Retranscription manuelle'
         },
    ]
}


@app.route('/')
def index():
    return render_template('index.html',
                           is_mainpage=True,
                           page_title="Accueil",
                           map_data=MAP_NB_TO_DATA)


@app.route('/map/<map_nb>')
def show_map(map_nb):
    if MAP_NB_TO_DATA.get(str(abs(int(map_nb)))):
        return render_template(**MAP_NB_TO_DATA.get(str(abs(int(map_nb))), {}))
    return index()


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
    return render_template('mentions_legales.html',
                           page_title="Mentions légales",
                           map_data=MAP_NB_TO_DATA,
                           dict_data=DICT_DATA)


@app.route('/about/', methods=['GET'])
def about():
    return render_template('about.html',
                           page_title="A propos",
                           map_data=MAP_NB_TO_DATA)


@app.route('/encyclopedia/', methods=['GET'])
def encyclopedia():
    return render_template('encyclopedia.html',
                           page_title="Encyclopédie",
                           map_data=MAP_NB_TO_DATA)


@app.route('/map_desc/<map_id>', methods=['GET'])
def show_map_description(map_id):
    if not map_id.isdigit():
        return index()

    return render_template('map_desc.html',
                           map_id=map_id,
                           lines=MAP_NB_TO_DATA[map_id]['lines'],
                           button_url='/map/'+map_id,
                           page_title=MAP_NB_TO_DATA[map_id].get('title'),
                           page_accroche=MAP_NB_TO_DATA[map_id].get('accroche'),
                           map_data=MAP_NB_TO_DATA)
