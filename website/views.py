from json import load
from json.decoder import JSONDecodeError
import os
from pathlib import Path
from . import app
from flask import render_template, jsonify, request
from api_ext.clips import Clips
from api_ext import BadStatusError
from .map_desc import MAP_ID_TO_DATA, DICT_DATA

BASE_DIR = Path(__file__).resolve().parent.parent


@app.route('/')
def index():
    return render_template('index.html',
                           is_mainpage=True,
                           page_title="Accueil",
                           map_data=MAP_ID_TO_DATA)


@app.route('/map/<map_nb>')
def show_map(map_nb):
    if MAP_ID_TO_DATA.get(str(abs(int(map_nb)))):
        return render_template(**MAP_ID_TO_DATA.get(str(abs(int(map_nb))), {}))
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
        return jsonify({'Error':
                        f'FileNotFoundError: {filename} not found'})
    except JSONDecodeError:
        return jsonify({'Error':
                        f'JSONDecodeError: {filename} : format incorrect.'})


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
                           map_data=MAP_ID_TO_DATA,
                           dict_data=DICT_DATA)


@app.route('/about/', methods=['GET'])
def about():
    return render_template('about.html',
                           page_title="A propos",
                           map_data=MAP_ID_TO_DATA)


@app.route('/encyclopedia/', methods=['GET'])
def encyclopedia():
    return render_template('encyclopedia.html',
                           page_title="Encyclopédie",
                           map_data=MAP_ID_TO_DATA)


@app.route('/map_desc/<map_id>', methods=['GET'])
def show_map_description(map_id):
    if not map_id.isdigit():
        return index()

    return render_template('map_description.html',
                           map_id=map_id,
                           map_data=MAP_ID_TO_DATA)
