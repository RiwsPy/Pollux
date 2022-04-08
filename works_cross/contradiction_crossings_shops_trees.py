from . import Works_cross
from works.crossings import Crossings
from works.shops import Shops
from works.trees import Trees
from formats.geojson import Geojson, Feature


class Contradiction_c_s_t(Works_cross):
    def __init__(self):
        super().__init__([Crossings, Shops], [Trees])
        self.new_features = Geojson()

    def dump(self, filename: str = "", features: list = None) -> None:
        super().dump(features=self.new_features.features)

    def apply_algo(self):
        for blue_feature in self.teams[0].features:
            blue_position = blue_feature.position
            calc_night = not blue_feature['properties'].get('opening_hours')

            for red_feature in self.teams[1].features:
                geo_distance_between = blue_position.distance(red_feature.position)

                if geo_distance_between <= 25:
                    contradiction_node = Feature()
                    item_intensity = {'Jour': 0, 'Nuit': 0, 'Différence': 0, }
                    intensity_value = round(16 / geo_distance_between ** 2, 2)
                    item_intensity['Jour'] += intensity_value
                    if calc_night:
                        item_intensity['Nuit'] += intensity_value
                    item_intensity['Différence'] = item_intensity['Jour'] - item_intensity['Nuit']

                    contradiction_node.lat, contradiction_node.lng = (blue_position + red_feature.position) / 2
                    contradiction_node.values = item_intensity
                    self.new_features.features.append(contradiction_node)
