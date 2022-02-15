from flask import Flask
import os

app = Flask(__name__)
app.debug = os.getenv('ENV_DEV') == 'DVLP'

from . import views, elements
