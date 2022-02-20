from . import Works
from api_ext.smmag import Smmag


class Tc_stops(Works):
    filename = 'tc_stops'
    request_method = Smmag().call
    url = '/api/points/json?types=stops'
    query = ""
    COPYRIGHT_ORIGIN = Smmag.BASE_URL
    COPYRIGHT_LICENSE = 'ODbL'
