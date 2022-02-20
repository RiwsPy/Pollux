from json import load, loads
from json.decoder import JSONDecodeError
import os
from pathlib import Path
from . import app
from flask import render_template, jsonify, request
import requests

BASE_DIR = Path(__file__).resolve().parent.parent


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/map/')
def show_map():
    return render_template('map.html')


@app.route('/api/<filename>', methods=['GET'])
def print_json(filename):
    try:
        with open(os.path.join(BASE_DIR, 'db/' + filename), 'r') as file:
            return jsonify(load(file))
    except FileNotFoundError:
        return jsonify({'Error': f'FileNotFoundError: {filename} not found'})
    except JSONDecodeError:
        return jsonify({'Error': f'JSONDecodeError: {filename} : format incorrect.'})


@app.route('/clips/', methods=['POST'])
def clips_recommendation():
    req = requests.request(method='POST', url='https://pollux-clips.herokuapp.com/zone', data=request.data)
    if req.status_code == 200:
        return jsonify(req.json())

    return jsonify({"recommendation": "Erreur"})
