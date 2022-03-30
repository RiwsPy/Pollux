from . import Works
from api_ext.grenoble_alpes_metropole import Gam


class Lamps(Works):
    filename = "lamps"
    file_ext = "csv"
    COPYRIGHT_ORIGIN = Gam.BASE_URL
    COPYRIGHT_LICENSE = 'ODbL'
    fake_request = True

    def _can_be_output(self, obj: dict) -> bool:
        if super()._can_be_output(obj):
            return super()._can_be_output(obj) and obj['properties']["Lampe - Régime"]
