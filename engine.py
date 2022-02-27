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


def tree_crossing_conflict():
    tr = Trees()
    tr.load(tr.output_filename)

    cr = Crossings()
    cr.load(cr.output_filename)

    features = Geojson()
    for crossing in cr:
        cr_position = Position(crossing['geometry']['coordinates'])
        for tree in tr:
            distance_between = cr_position.distance(tree['geometry']['coordinates'])
            if distance_between <= 25:
                new_feature = Feature()
                new_feature.lat, new_feature.lng = (cr_position + tree['geometry']['coordinates'])/2
                new_feature.intensity = 1- (distance_between/25)
                features.append(new_feature)
    with open(os.path.join(BASE_DIR, 'db/conflict_tree_crossing.json'), 'w') as file:
        dump(features, file)


def tree_shop_conflict():
    tr = Trees()
    tr.load(tr.output_filename)

    cr = Shops()
    cr.load(cr.output_filename)

    features = Geojson()
    for crossing in cr:
        cr_position = Position(crossing['geometry']['coordinates'])
        for tree in tr:
            distance_between = cr_position.distance(tree['geometry']['coordinates'])
            if distance_between <= 25:
                new_feature = Feature()
                new_feature.lat, new_feature.lng = (cr_position + tree['geometry']['coordinates'])/2
                new_feature.intensity = 1- (distance_between/25)
                features.append(new_feature)
    with open(os.path.join(BASE_DIR, 'db/conflict_tree_shop.json'), 'w') as file:
        dump(features, file)


if __name__ == '__main__':
    #update_db_after_map_position()
    #tree_crossing_conflict()
    app.run()
    #tree_shop_conflict()
