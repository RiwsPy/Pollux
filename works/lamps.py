from . import Works
from api_ext.grenoble_alpes_metropole import Gam

lowering_night_impact = {
    "CREM NOCTURNE AVEC REDUCTION 33% flux - 33 % NRJ en milieu de nuit (LED)": 33,
    "CREM NOCTURE AVEC REDUCTION 50% flux - 40 % NRJ en milieu de nuit": 50,
    "CREM NOCTURNE AVEC REDUCTION 50% flux - 50 % NRJ en milieu de nuit (LED)": 50,
    "GRE NOCTURNE AVEC REDUCTION Bi-Pw (Réduction de 30% de 22h40 à 5h40)": 30,
    "GRE NOCTURNE AVEC REDUCTION VARIATEUR LUBIO (Réduction de 30 % de 23h à 6h)": 30,
    "CREM NOCTURNE AVEC VARIATIEUR BH (Réduction de  33 % flux - 27 % puissance de 22h à 6h)": 33,
}


class Lamps(Works):
    filename = "lamps"
    file_ext = "csv"
    COPYRIGHT_ORIGIN = Gam.BASE_URL
    COPYRIGHT_LICENSE = 'ODbL'
    fake_request = True

    def _can_be_output(self, obj: dict, bound=None) -> bool:
        return super()._can_be_output(obj, bound) and obj['properties']["Lampe - Régime"]

    class Model(Works.Model):
        @property
        def id(self) -> int:
            return self.properties["Luminaire - Code luminaire"]

        @property
        def source(self) -> str:
            return 'local knowledge'

        @property
        def __dict__(self) -> dict:
            methods = ('id', 'source')
            return {method: self[method] for method in methods}

        @property
        def height(self) -> float:
            return float(self.properties.get("Luminaire - Hauteur de feu") or "8")

        @property
        def irc(self) -> int:
            return int(self.properties.get('Lampe - IRC') or '75')

        @property
        def colour(self) -> int:
            return int(self.properties.get('Lampe - Température Couleur') or '5000')

        @property
        def on_motion(self) -> bool:
            return self.properties.get("Lampe - Régime (simplifié)") == "Détéction en milieu de nuit"

        @property
        def lowering_night(self) -> int:
            return lowering_night_impact.get(self.properties['Lampe - Régime'], 0)
