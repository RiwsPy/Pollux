from . import Works
from api_ext.grenoble_alpes_metropole import Gam


class Lamps(Works):
    filename = "lamps"
    file_ext = "csv"
    COPYRIGHT_ORIGIN = Gam.BASE_URL
    COPYRIGHT_LICENSE = 'ODbL'

    def _can_be_output(self, obj: dict) -> bool:
        if super()._can_be_output(obj):
            return super()._can_be_output(obj) and obj['properties']["Lampe - Régime"]

    def request(self, **kwargs) -> dict:
        self.load()
        return self


class Lamps_day(Lamps):
    filename = "lamps_day"
    file_ext = "json"

    def _can_be_output(self, obj: dict) -> bool:
        return super()._can_be_output(obj) and\
                int(obj['properties'].get("Lampe - Température Couleur", "5000")) > 2500

    def load(self, filename: str = '', file_ext: str = '') -> None:
        super().load(filename=super().output_filename)


class Lamps_night(Lamps_day):
    filename = "lamps_night"
    file_ext = "json"

    def _can_be_output(self, obj: dict) -> bool:
        return super()._can_be_output(obj) and\
               obj['properties']["Lampe - Régime (simplifié)"] != "Abaissement en milieu de nuit" and\
               obj['properties']["Lampe - Régime (simplifié)"] != "Détéction en milieu de nuit"
