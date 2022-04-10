#!/usr/bin/env python
from works.trees import Trees
from works.crossings import Crossings
from works.birds import Birds
from works.parks import Parks
from works.shops import Shops
from works.tc_ways import Tc_ways
from works.tc_stops import Tc_stops
from works.highways import Highways
from works.lamps import Lamps
from website import app
from works.accidents import Accidents
from dotenv import load_dotenv
from pathlib import Path
import argparse

load_dotenv()
BASE_DIR = Path(__file__).resolve().parent
db_classes = (Crossings,
              Parks,
              Shops,
              Tc_stops,
              Tc_ways,
              Trees,
              Accidents,
              Birds,
              Lamps,
              Highways
              )


def full_update():
    for cls_type in db_classes:
        update(cls_type)
    print('Mise à jour terminée.')


def update(cls_type):
    print(cls_type, 'en cours.')
    try:
        cls_instance = cls_type()
        data = cls_instance.request()
        cls_instance.update(data)
        if cls_instance.fake_request is False:
            cls_instance.dump()  # save request result
        cls_instance.output()  # filter on request result and save it
    except FileNotFoundError:
        print('Error', cls_type, ': FileNotFound')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Pollux - Fonctionnalités.')
    parser.add_argument("-uDB", "--updateDB",
                        nargs='*',
                        choices=['all'] + [cls.filename for cls in db_classes],
                        help="Mettre à jour les bases de données de l'application.")
    args = parser.parse_args()

    if args.updateDB is not None:
        db_args = [arg.lower() for arg in args.updateDB]
        if not db_args or "all" in db_args:
            full_update()
        else:
            for cls in set(db_classes).intersection(set(db_args)):
                update(cls)
    else:
        # team_conflict(blue_team=[Trees, Birds], red_team=[Lamps])
        # team_contradiction(blue_team=[Crossings, Shops], red_team=[Trees, Birds])

        app.run()

        # w = Impact_crossing_lamp()
        # w.apply_algo()
        # w.dump()
