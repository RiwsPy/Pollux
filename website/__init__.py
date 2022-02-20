from flask import Flask
import os

app = Flask(__name__)
app.debug = os.getenv('ENV_DEV') == 'DVLP'
app = Flask(__name__)


from . import views
