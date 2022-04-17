from . import Works_cross
from works import lamp, tree


class Cross(Works_cross):
    def __init__(self):
        super().__init__([lamp], [tree])

    def dump(self, filename: str = "", features: list = None) -> None:
        super().dump(features=self.teams[0].features)

    def apply_algo(self):
        for lamp in self.teams[0].features:
            lamp_position = lamp.position
            lamp_case = self.feature_position_case(lamp)
            lamp_height = lamp['properties']['height']
            lamp['values'] = {'Base': 0, 'Jour': 0, 'Nuit': 0}

            calc_day = lamp.colour > 2500 and not lamp.on_motion
            night_impact = 100 - lamp.lowering_night
            for i in range(lamp_case[0]-1, lamp_case[0]+2):
                for j in range(lamp_case[1]-1, lamp_case[1]+2):
                    try:
                        trees = self.teams_array[1][(i, j)]
                    except IndexError:
                        continue
                    else:
                        if not trees:
                            continue

                        for tree in trees:
                            geo_distance_between = lamp_position.distance(tree.position)
                            diff_lum_tree_height = max(lamp_height - tree.height, 0)
                            square_distance = diff_lum_tree_height ** 2 + geo_distance_between ** 2
                            if square_distance <= 25 ** 2:
                                # valeur multipliée par 9 pour avoir des valeurs comprises entre 0 et 1
                                # TODO: à revoir
                                intensity_value = 9 / square_distance
                                lamp['values']['Base'] += intensity_value
                                if calc_day:
                                    lamp['values']['Jour'] += intensity_value
                                    lamp['values']['Nuit'] += intensity_value * night_impact / 100

            for data in lamp['values']:
                lamp['values'][data] = round(lamp['values'][data], 2)
