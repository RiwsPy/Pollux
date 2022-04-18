#!/usr/bin/env python
from website import app
from dotenv import load_dotenv
from pathlib import Path
import argparse
from importlib import import_module
import os
from works import lamp

load_dotenv()
BASE_DIR = Path(__file__).resolve().parent

WORKS_CLS = []
works_file = os.listdir(os.path.join(BASE_DIR, 'works'))
works_file.remove('__init__.py')

for file in sorted(works_file):
    cls, _, ext = file.rpartition('.')
    if ext != 'py':
        continue

    cls = import_module('works.' + cls).Works
    WORKS_CLS.append({'cls': cls, 'filename': cls.filename})

WORKS_CROSS_CLS = []
works_cross_file = os.listdir(os.path.join(BASE_DIR, 'works/cross'))
works_cross_file.remove('__init__.py')

for file in sorted(works_cross_file):
    cls, _, ext = file.rpartition('.')
    if ext != 'py':
        continue

    cls = import_module('works.cross.' + cls).Cross
    WORKS_CROSS_CLS.append({'cls': cls, 'filename': file})


def full_db_update():
    for cls_type in WORKS_CLS:
        db_update(cls_type)


def db_update(cls_type):
    cls_instance = cls_type()
    print(cls_instance.filename, 'en cours.')
    try:
        data = cls_instance.request()
        cls_instance.output(data)  # filter on request result and save it
    except FileNotFoundError:
        print('Error', cls_type, ': FileNotFound')


def full_db_cross_update():
    for cls_type in WORKS_CROSS_CLS:
        db_cross_update(cls_type)


def db_cross_update(cls_type):
    cls_instance = cls_type()
    print(cls_instance, 'en cours.')
    try:
        cls_instance.apply_algo()
        cls_instance.dump()
    except FileNotFoundError:
        print('Error', cls_type, ': FileNotFound')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Pollux - Fonctionnalités.')
    parser.add_argument("-uDB", "--updateDB",
                        nargs='*',
                        choices=['all'] + [cls['filename'] for cls in WORKS_CLS],
                        help="Mettre à jour les bases de données de l'application.")
    parser.add_argument("-uCDB", "--updateCrossDB",
                        nargs='*',
                        choices=['all'] + [cls['filename'] for cls in WORKS_CROSS_CLS],
                        help="Appliquer un algorithme pour mettre à jour une base de données croisée.")
    args = parser.parse_args()

    if args.updateDB is not None:
        db_args = [arg.lower() for arg in args.updateDB]
        if not db_args or "all" in db_args:
            full_db_update()
        else:
            for cls_data in WORKS_CLS:
                if cls_data['filename'] in db_args:
                    db_update(cls_data['cls'])
        print('Mise à jour terminée.')
    elif args.updateCrossDB is not None:
        db_args = [arg.lower() for arg in args.updateCrossDB]
        if not db_args or "all" in db_args:
            full_db_cross_update()
        else:
            for cls_data in WORKS_CROSS_CLS:
                if cls_data['filename'] in db_args:
                    db_cross_update(cls_data['cls'])
        print('Mise à jour terminée.')
    else:
        app.run()
