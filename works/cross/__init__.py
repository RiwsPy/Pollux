from formats.geojson import Geojson, Geo_Feature
from works import BASE_DIR, Default_works
import os
import json
from typing import List
from formats.position import LNG_1M, LAT_1M, Relation
from math import ceil, floor
import numpy as np
from collections import defaultdict


class Works_cross:
    value_attr = '_pollux_values'
    max_range = 25
    multiplier = 1

    # Works_cross(input=[[teammate1, teammate2], [teammate1], [teammate1], ...])
    def __init__(self, *teams, bound: List[float] = None):
        self.bound = bound or Default_works.DEFAULT_BOUND

        dim = bound_to_array(self.bound, self.max_range)
        self.teams = []
        self.teams_array = []
        self.copyrights = set()
        for team in teams:
            if not team:
                continue

            np_array = np.empty(dim, dtype=np.dtype('O'))
            team_data = Geojson(name='')
            team_names = []
            team_cpr = set()
            for works_cls in team:
                team_works = works_cls.Works(bound=self.bound)
                data = team_works.load(team_works.output_filename, 'json')
                geo = Geojson(COPYRIGHT=team_works.COPYRIGHT)
                geo.extend(data['features'])
                new_features = team_works.bound_filter(geo).features
                if new_features:
                    np_array = self.repartition_in_array(new_features, np_array)
                    team_data.extend(new_features)
                    team_names.append(team_works.filename)
                    team_cpr.add(team_works.COPYRIGHT)
                    self.copyrights.add(team_works.COPYRIGHT)
            self.teams_array.append(np_array)
            team_data.name = '-'.join(team_names)
            team_data.COPYRIGHT = ' -- '.join(team_cpr)
            self.teams.append(team_data)

    def _iter_double_and_range(self):
        for team in self.teams:
            for teammate in team.features:
                teammate.position = teammate.position.force_position()
                teammate['geometry']['type'] = teammate.type_of_pos()
                teammate[self.value_attr] = defaultdict(int)

        for blue_teammate in self.teams[0].features:
            blue_position = blue_teammate.position
            blue_case = self.feature_position_case(blue_teammate)

            for i in range(blue_case[0]-1, blue_case[0]+2):
                for j in range(blue_case[1]-1, blue_case[1]+2):
                    try:
                        red_features = self.teams_array[1][(i, j)] or ()
                    except IndexError:
                        continue
                    else:
                        for red_teammate in red_features:
                            geo_distance_between = blue_position.distance(red_teammate.position)
                            if geo_distance_between <= self.max_range:
                                yield blue_teammate, red_teammate, geo_distance_between

    @property
    def db_name(self) -> str:
        return '--'.join(team.name for team in self.teams)

    @property
    def COPYRIGHT(self) -> str:
        return ' || '.join(self.copyrights)

    @property
    def features(self) -> list:
        ret = []
        for team in self.teams:
            ret.extend(team.features)
        return ret

    def dump(self, filename: str = "", features: list = None) -> None:
        print(f'Ecriture de db/cross/{filename or self.db_name + ".json"}')
        with open(os.path.join(BASE_DIR, f'db/cross/{filename or self.db_name + ".json"}'),
                  'w') as file:
            json.dump(Geojson(COPYRIGHT=self.COPYRIGHT, features=features or self.features),
                      file,
                      ensure_ascii=False,
                      indent=1)

    def apply_algo(self) -> None:
        pass

    def feature_position_case(self, feature):
        lat_min, lng_min, lat_max, lng_max = self.bound
        try:
            test = feature.position.lat
            position = feature.position
        except IndexError:
            position = Relation(feature.position).to_position()

        height = floor((position.lat - lat_min) / LAT_1M / self.max_range)
        width = floor((position.lng - lng_min) / LNG_1M / self.max_range)
        return height, width

    def repartition_in_array(self, features, array):
        for feature in features:
            case = self.feature_position_case(feature)
            try:
                if array[case]:
                    array[case].append(feature)
                else:
                    array[case] = [feature]
            except IndexError:
                print(case, 'out of bound')
                continue
        return array


def bound_to_array(bound: List[float], side: int) -> tuple:
    lat_min, lng_min, lat_max, lng_max = bound
    height = (lat_max - lat_min) / LAT_1M / side
    width = (lng_max - lng_min) / LNG_1M / side
    return ceil(height), ceil(width)
