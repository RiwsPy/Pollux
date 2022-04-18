from . import Works_cross
from works import lamp, crossing


class Cross(Works_cross):
    max_range = 25
    filename = __file__

    def __init__(self):
        super().__init__([crossing], [lamp])

    def dump(self, filename: str = "", features: list = None) -> None:
        super().dump(features=self.teams[0].features)

    def apply_algo(self):
        # en fonction de la distance et de l'IRC du luminaire
        for blue_teammate, red_teammate, distance in self._iter_double_and_range():
            square_distance = red_teammate.height ** 2 + distance ** 2
            if square_distance <= self.max_range ** 2:
                night_impact = 100 - red_teammate.lowering_night

                intensity_value = red_teammate.irc / square_distance
                blue_teammate['properties'][self.value_attr]['Jour'] += intensity_value
                blue_teammate['properties'][self.value_attr]['Nuit'] += intensity_value*night_impact/100
                blue_teammate['properties'][self.value_attr]['Différence'] += intensity_value - intensity_value*night_impact/100
