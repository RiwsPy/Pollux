from . import Works, BASE_DIR
import os
from formats.csv import convert_to_geojson
from api_ext.grenoble_alpes_metropole import Gam


class Lamps(Works):
    filename = "lamps2"
    file_ext = "csv"
    COPYRIGHT_ORIGIN = Gam.BASE_URL
    COPYRIGHT_LICENSE = 'ODbL'

    def load(self, filename: str = '', file_ext: str = '') -> None:
        filename = filename or self.filename
        with open(os.path.join(BASE_DIR, f'db/{filename}.{file_ext or self.file_ext}'), 'r') as file:
            self.update(convert_to_geojson(file))

    def _can_be_output(self, obj: dict) -> bool:
        return super()._can_be_output(obj) and obj['properties']["Lampe - Régime"]


class Lamps_night(Lamps):
    filename = "lamps2_night"
    file_ext = "json"

    def _can_be_output(self, obj: dict) -> bool:
        return super()._can_be_output(obj) and \
               (not obj['properties']["Lampe - Température Couleur"] or
                int(obj['properties']["Lampe - Température Couleur"]) > 2500) and\
               obj['properties']["Lampe - Régime (simplifié)"] != "Abaissement en milieu de nuit" and \
               obj['properties']["Lampe - Régime (simplifié)"] != "Détéction en milieu de nuit"

