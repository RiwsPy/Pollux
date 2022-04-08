from . import Works_cross
from works.lamps import Lamps
from works.trees import Trees


class Impact_trees_lamps(Works_cross):
    def __init__(self):
        super().__init__([Trees], [Lamps])

    def dump(self, filename: str = "", features: list = None) -> None:
        super().dump(features=self.teams[0].features)

    def apply_algo(self):
        for tree in self.teams[0].features:
            tree_position = tree.position
            tree_height = tree.height
            tree['values'] = {'Base': 0, 'Jour': 0, 'Nuit': 0}

            for lamp in self.teams[1].features:
                geo_distance_between = tree_position.distance(lamp.position)
                diff_lum_tree_height = max(lamp.height - tree_height, 0)
                square_distance = diff_lum_tree_height ** 2 + geo_distance_between ** 2
                if square_distance <= 25 ** 2:
                    # valeur multipliée par 9 pour avoir des valeurs comprises entre 0 et 1
                    # TODO: à revoir

                    calc_day = lamp.colour > 2500 and not lamp.on_motion
                    night_impact = 100 - lamp.lowering_night

                    intensity_value = 9 / square_distance
                    tree['values']['Base'] += intensity_value
                    if calc_day:
                        tree['values']['Jour'] += intensity_value
                        tree['values']['Nuit'] += intensity_value*night_impact/100
