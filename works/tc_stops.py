from . import Works
from api_ext import smmag


class Tc_stops(Works):
    filename = 'tc_stops'
    request_method = smmag.call
    url = '/api/points/json?types=stops'
    query = ""
    COPYRIGHT_ORIGIN = smmag.BASE_URL
    COPYRIGHT_LICENSE = 'ODbL'
