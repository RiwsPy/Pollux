#!/usr/bin/env python
from works.trees import Trees
from works.crossings import Crossings
from works.birds import Birds
from works.parks import Parks
from works.shops import Shops
from works.tc_ways import Tc_ways
from works.tc_stops import Tc_stops
from website import app
from works.accidents import Accidents
from dotenv import load_dotenv
from formats.position import Position
from formats.geojson import Geojson, Feature
from pathlib import Path
import os
from json import dump

load_dotenv()
BASE_DIR = Path(__file__).resolve().parent


def update_db_after_map_position():
    cls_set_with_req = (Crossings, Parks, Shops, Tc_stops, Tc_ways, Trees)
    cls_set_load_without_request = (Accidents, Birds)
    for cls_type in cls_set_with_req:
        print(cls_type, 'en cours.')
        cls_instance = cls_type()
        data = cls_instance.request()
        cls_instance.update(data)
        cls_instance.dump()
        cls_instance.output()

    for cls_type in cls_set_load_without_request:
        print(cls_type, 'en cours.')
        cls_instance = cls_type()
        cls_instance.load()
        cls_instance.output()


def team_conflict(blue_team: list, red_team: list) -> None:
    if not blue_team or not red_team:
        return None

    cls_blue_leader = blue_team[0]
    blue_features = cls_blue_leader()
    blue_features.load(blue_features.output_filename)
    blue_team_name = blue_features.filename
    for cls_type in blue_team[1:]:
        blue_member = cls_type()
        blue_member.load(blue_member.output_filename)
        blue_features['features'].extend(blue_member['features'])
        blue_team_name += '_' + blue_member.filename

    cls_red_leader = red_team[0]
    red_features = cls_red_leader()
    red_features.load(red_features.output_filename)
    red_team_name = red_features.filename
    for cls_type in red_team[1:]:
        red_member = cls_type()
        red_member.load(red_member.output_filename)
        red_features['features'].extend(red_member['features'])
        red_team_name += '_' + red_features.filename

    features = Geojson()
    for blue_feature in blue_features:
        cr_position = Position(blue_feature['geometry']['coordinates'])
        for red_feature in red_features:
            distance_between = cr_position.distance(red_feature['geometry']['coordinates'])
            if distance_between <= 25:
                new_feature = Feature()
                new_feature.lat, new_feature.lng = (cr_position + red_feature['geometry']['coordinates'])/2
                new_feature.intensity = 1 - (distance_between/25)
                features.append(new_feature)

    with open(os.path.join(BASE_DIR, 'db/' + blue_team_name + '__' + red_team_name + '.json'), 'w+') as file:
        dump(features, file)


if __name__ == '__main__':
    #update_db_after_map_position()
    #team_conflict(blue_team=[Shops], red_team=[Trees])
    #team_conflict(blue_team=[Crossings, Shops], red_team=[Trees])
    #team_conflict(blue_team=[Crossings], red_team=[Trees])
    app.run()
