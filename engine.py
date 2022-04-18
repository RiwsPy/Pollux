#!/usr/bin/env python
from website import app
from dotenv import load_dotenv
from pathlib import Path
import argparse
from importlib import import_module
import os

load_dotenv()
BASE_DIR = Path(__file__).resolve().parent


def db_update(cls_type):
    cls_instance = cls_type()
    print(cls_instance.filename, 'en cours.')
    try:
        data = cls_instance.request()
        cls_instance.output(data)  # filter on request result and save it
    except FileNotFoundError:
        print('Error', cls_type, ': FileNotFound')


def db_cross_update(cls_type):
    cls_instance = cls_type()
    print(cls_instance, 'en cours.')
    try:
        cls_instance.load()
        cls_instance.apply_algo()
        cls_instance.dump()
    except FileNotFoundError:
        print('Error', cls_type, ': FileNotFound')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Pollux - Fonctionnalités.')
    parser.add_argument("-uDB", "--updateDB",
                        nargs='*',
                        help="Mettre à jour les bases de données de l'application.")
    parser.add_argument("-uCDB", "--updateCrossDB",
                        nargs='*',
                        help="Appliquer un algorithme pour mettre à jour une base de données croisée.")
    args = parser.parse_args()

    if args.updateDB is not None:
        db_args = args.updateDB
        for db_arg in db_args:
            arg = db_arg.replace('.py', '').replace('/', '.')
            try:
                cls = import_module(arg).Works
            except ModuleNotFoundError:
                print(f'Module {arg} introuvable.')
            except AttributeError:
                print(f'Classe {arg}.Works introuvable.')
            else:
                db_update(cls)
        print('Mise à jour terminée.')
    elif args.updateCrossDB is not None:
        for db_arg in args.updateCrossDB:
            arg = db_arg.replace('.py', '').replace('/', '.')
            try:
                cls = import_module(arg).Cross
            except ModuleNotFoundError:
                print(f'Module {arg} introuvable.')
            except AttributeError:
                print(f'Classe {arg}.Cross introuvable.')
            else:
                db_cross_update(cls)
        print('Mise à jour terminée.')
    else:
        app.run()
