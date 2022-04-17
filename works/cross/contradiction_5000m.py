from . import Works_cross
from works import church, vending_machine


class Cross(Works_cross):
    side = 5000

    def __init__(self):
        super().__init__([church], [vending_machine])

    def dump(self, filename: str = "", features: list = None) -> None:
        super().dump(features=self.teams[0].features)

    def apply_algo(self):
        for blue_teammate in self.teams[0].features:
            blue_teammate.position = blue_teammate.position.force_position()
            blue_teammate['geometry']['type'] = blue_teammate.type_of_pos()
            blue_position = blue_teammate.position
            blue_case = self.feature_position_case(blue_teammate)
            blue_teammate['values'] = {'Contradiction': 0}

            for i in range(blue_case[0]-1, blue_case[0]+2):
                for j in range(blue_case[1]-1, blue_case[1]+2):
                    try:
                        machines = self.teams_array[1][(i, j)]
                    except IndexError:
                        continue
                    else:
                        for machine in machines or ():
                            geo_distance_between = blue_position.distance(machine.position)
                            if geo_distance_between <= self.side:
                                intensity_value = 100 / geo_distance_between
                                blue_teammate['values']['Contradiction'] += intensity_value

            for data in blue_teammate['values']:
                blue_teammate['values'][data] = round(blue_teammate['values'][data], 2)
