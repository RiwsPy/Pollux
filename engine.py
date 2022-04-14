#!/usr/bin/env python
from website import app
from dotenv import load_dotenv
from pathlib import Path
import argparse
from importlib import import_module
import os

load_dotenv()
BASE_DIR = Path(__file__).resolve().parent

WORKS_CLS = []
WORKS_CLS_FILENAME = []
works_file = os.listdir(os.path.join(BASE_DIR, 'works'))
works_file.remove('__init__.py')

for file in sorted(works_file):
    cls, _, ext = file.rpartition('.')
    if ext != 'py':
        continue

    cls = import_module('works.' + cls).Works
    WORKS_CLS.append({'cls': cls, 'filename': cls.filename})


def full_update():
    for cls_type in WORKS_CLS:
        update(cls_type)


def update(cls_type):
    cls_instance = cls_type()
    print(cls_instance.filename, 'en cours.')
    try:
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
                        choices=['all'] + [cls['filename'] for cls in WORKS_CLS],
                        help="Mettre à jour les bases de données de l'application.")
    args = parser.parse_args()

    if args.updateDB is not None:
        db_args = [arg.lower() for arg in args.updateDB]
        if not db_args or "all" in db_args:
            full_update()
        else:
            for cls_data in WORKS_CLS:
                if cls_data['filename'] in db_args:
                    update(cls_data['cls'])
        print('Mise à jour terminée.')
    else:
        # team_conflict(blue_team=[Trees, Birds], red_team=[Lamps])
        # team_contradiction(blue_team=[Crossings, Shops], red_team=[Trees, Birds])

        app.run()
        # w = Highways()
        # w.load()
        # w.output()

        # w = Impact_crossing_lamp()
        # w.apply_algo()
        # w.dump()