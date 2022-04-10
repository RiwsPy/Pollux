from . import Works_cross
from works.lamps import Lamps
from works.crossings import Crossings


class Impact_crossing_lamp(Works_cross):
    def __init__(self):
        super().__init__([Crossings], [Lamps])

    def dump(self, filename: str = "", features: list = None) -> None:
        super().dump(features=self.teams[0].features)

    def apply_algo(self):
        # en fonction de la distance et de l'IRC du luminaire
        for blue_feature in self.teams[0].features:
            blue_position = blue_feature.position
            blue_feature['values'] = {'Jour': 0, 'Nuit': 0}

            for lamp in self.teams[1].features:
                geo_distance_between = blue_position.distance(lamp.position)
                square_distance = lamp.height ** 2 + geo_distance_between ** 2
                if square_distance <= 25 ** 2:
                    night_impact = 100 - lamp.lowering_night

                    intensity_value = lamp.irc / square_distance
                    blue_feature['values']['Jour'] += intensity_value
                    blue_feature['values']['Nuit'] += intensity_value*night_impact/100

            for data in blue_feature['values']:
                blue_feature['values'][data] = round(blue_feature['values'][data], 2)
