from . import Works, LNG_MAX, LNG_MIN, LAT_MIN, LAT_MAX
from api_ext.smmag import Smmag


class Tc_ways(Works):
    filename = 'tc_ways'
    request_method = Smmag().call
    url = '/api/lines/json?types=ligne&reseaux=SEM'  # TODO: ajouter les trams ?
    query = ""
    COPYRIGHT_ORIGIN = Smmag.BASE_URL
    COPYRIGHT_LICENSE = 'ODbL'

    def _can_be_output(self, obj: dict) -> bool:
        if obj['geometry']:
            for lines in obj['geometry']['coordinates']:
                for obj_lng, obj_lat in lines:
                    if LAT_MIN <= obj_lat <= LAT_MAX and LNG_MIN <= obj_lng <= LNG_MAX:
                        return True
        return False
