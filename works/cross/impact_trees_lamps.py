from . import Works_cross
from works import lamp, tree


class Cross(Works_cross):
    def __init__(self):
        super().__init__([tree], [lamp])

    def dump(self, filename: str = "", features: list = None) -> None:
        super().dump(features=self.teams[0].features)

    def apply_algo(self):
        for tree in self.teams[0].features:
            tree_position = tree.position
            tree_height = tree.height
            tree_case = self.feature_position_case(tree)

            tree['values'] = {'Base': 0, 'Jour': 0, 'Nuit': 0}
            for i in range(tree_case[0]-1, tree_case[0]+2):
                for j in range(tree_case[1]-1, tree_case[1]+2):
                    try:
                        lamps = self.teams_array[1][(i, j)]
                    except IndexError:
                        continue
                    else:
                        if not lamps:
                            continue

                        for lamp in lamps:
                            geo_distance_between = tree_position.distance(lamp.position)
                            diff_lum_tree_height = max(lamp.height - tree_height, 0)
                            square_distance = diff_lum_tree_height ** 2 + geo_distance_between ** 2
                            if square_distance <= 25 ** 2:
                                # valeur multipliée par 9 pour avoir des valeurs comprises entre 0 et 1
                                # TODO: à revoir

                                calc_day = lamp.colour > 2500 and not lamp.on_motion
                                night_impact = 100 - lamp.lowering_night

                                intensity_value = 9 / square_distance
                                tree['values']['Base'] += round(intensity_value, 2)
                                if calc_day:
                                    tree['values']['Jour'] += round(intensity_value, 2)
                                    tree['values']['Nuit'] += round(intensity_value*night_impact/100, 2)

            for data in tree["values"]:
                tree['values'][data] = round(tree['values'][data], 2)
