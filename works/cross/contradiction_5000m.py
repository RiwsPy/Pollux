from . import Works_cross
from works import church, vending_machine


class Cross(Works_cross):
    def __init__(self):
        super().__init__([church], [vending_machine])

    def dump(self, filename: str = "", features: list = None) -> None:
        super().dump(features=self.teams[0].features)

    def apply_algo(self):
        for church_elt in self.teams[0].features:
            church_position = church_elt.position
            church_elt['values'] = {'Contradiction': 0}

            for lamp in self.teams[1].features:
                geo_distance_between = church_position.distance(lamp.position)
                if geo_distance_between <= 5000:
                    intensity_value = 1000 / geo_distance_between
                    church_elt['values']['Contradiction'] = round(intensity_value, 2)
