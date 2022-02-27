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

load_dotenv()


def update_db_after_map_position():
    cls_set_with_req = (Crossings, Parks, Shops, Tc_stops, Tc_ways)
    cls_set_load_without_request = (Accidents, Birds, Trees)
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


if __name__ == '__main__':
    app.run()
    #update_db_after_map_position()
