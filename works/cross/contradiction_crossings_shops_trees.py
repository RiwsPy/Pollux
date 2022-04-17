from . import Works_cross
from works import crossing, shop, tree
from formats.geojson import Geojson, Geo_Feature


class Cross(Works_cross):
    side = 25

    def __init__(self):
        super().__init__([crossing, shop], [tree])
        self.new_features = Geojson()

    def dump(self, filename: str = "", features: list = None) -> None:
        super().dump(features=self.new_features.features)

    def apply_algo(self):
        for blue_feature in self.teams[0].features:
            blue_position = blue_feature.position
            blue_case = self.feature_position_case(blue_feature)
            calc_night = not blue_feature['properties'].get('opening_hours')

            for i in range(blue_case[0]-1, blue_case[0]+2):
                for j in range(blue_case[1]-1, blue_case[1]+2):
                    try:
                        red_features = self.teams_array[1][(i, j)]
                    except IndexError:
                        continue
                    else:
                        for red_feature in red_features or ():
                            geo_distance_between = blue_position.distance(red_feature.position)
                            if geo_distance_between > self.side:
                                continue

                            contradiction_node = Geo_Feature()
                            item_intensity = {'Jour': 0, 'Nuit': 0, 'Différence': 0, }
                            intensity_value = round(16 / geo_distance_between ** 2, 2)
                            item_intensity['Jour'] += intensity_value
                            if calc_night:
                                item_intensity['Nuit'] += intensity_value
                            item_intensity['Différence'] = item_intensity['Jour'] - item_intensity['Nuit']

                            contradiction_node.lat, contradiction_node.lng = (blue_position + red_feature.position) / 2
                            contradiction_node.values = item_intensity
                            self.new_features.features.append(contradiction_node)
