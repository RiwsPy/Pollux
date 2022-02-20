from . import Works
from api_ext.grenoble_alpes_metropole import Gam


class Trees(Works):
    filename = 'trees'
    request_method = Gam().call
    url = '/opendata/38185-GRE/EspacePublic/json/ARBRES_TERRITOIRE_VDG_EPSG4326.json'
    query = ""
    COPYRIGHT_ORIGIN = Gam.BASE_URL
    COPYRIGHT_LICENSE = 'ODbL'
