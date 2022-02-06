from . import Works
from api_ext import grenoble_alpes_metropole


class Trees(Works):
    filename = 'trees'
    request_method = grenoble_alpes_metropole.call
    url = 'opendata/38185-GRE/EspacePublic/json/ARBRES_TERRITOIRE_VDG_EPSG4326.json'
    query = ""
    COPYRIGHT_ORIGIN = 'www.metropolegrenoble.org'
    COPYRIGHT_LICENSE = 'OBdL'
