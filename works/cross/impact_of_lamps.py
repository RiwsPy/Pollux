from . import Works_cross
from works import lamp, tree


class Cross(Works_cross):
    max_range = 25
    multiplier = 9
    filename = __file__

    def __init__(self):
        super().__init__([lamp], [tree])

    def dump(self, filename: str = "", features: list = None) -> None:
        super().dump(features=self.teams[0].features)

    def apply_algo(self):
        for blue_teammate, red_teammate, distance in self._iter_double_and_range():
            diff_lum_tree_height = max(blue_teammate.height - red_teammate.height, 0)
            square_distance = diff_lum_tree_height ** 2 + distance ** 2
            if square_distance <= self.max_range ** 2:
                intensity_value = self.multiplier / square_distance
                blue_teammate['properties'][self.value_attr]['Base'] += intensity_value

                if blue_teammate.colour <= 2500 or blue_teammate.on_motion:
                    continue

                blue_teammate['properties'][self.value_attr]['Jour'] += intensity_value
                blue_teammate['properties'][self.value_attr]['Nuit'] += intensity_value * (1 - blue_teammate.lowering_night / 100)
                blue_teammate['properties'][self.value_attr]['Différence'] += intensity_value* (1 - (1 - blue_teammate.lowering_night / 100))
