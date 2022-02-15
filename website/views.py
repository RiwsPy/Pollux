from json import load
import os
from pathlib import Path
from . import app
from flask import render_template, jsonify
from . import elements

BASE_DIR = Path(__file__).resolve().parent.parent


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/map/')
def show_map():
    return render_template('map.html')


@app.route('/ipycarte')
def ipycarte():
    elements.elements_map()
    return render_template('elements_map.html')


@app.route('/api/<filename>', methods=['GET'])
def print_json(filename):
    try:
        with open(os.path.join(BASE_DIR, 'db/' + filename), 'r') as file:
            return jsonify(load(file))
    except FileNotFoundError:
        return jsonify({'Error': f'FileNotFoundError: {filename} not found'})
