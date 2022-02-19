from json import load, loads
from json.decoder import JSONDecodeError
import os
from pathlib import Path
from . import app
from flask import render_template, jsonify, request

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
    #data = loads(request.data.decode('utf-8'))
    return jsonify({"recommendations": "Test ok é_è\nVoit tout ce qu'il y a à dire !"})
