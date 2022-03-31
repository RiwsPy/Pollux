#!/usr/bin/env python
from works import Works
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
from formats.geojson import Geojson
from formats.position import Position
from pathlib import Path
import argparse
from typing import Tuple

load_dotenv()
BASE_DIR = Path(__file__).resolve().parent
db_classes = (Crossings, Parks, Shops, Tc_stops, Tc_ways, Trees, Accidents, Birds, Lamps, Highways)


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


# TODO: replacer ce bazar
def create_teams(blue_team: list, red_team: list) -> Tuple[dict, str, dict, str]:
    cls_blue_leader = blue_team[0]
    blue_features = cls_blue_leader()
    blue_features.load(blue_features.output_filename, file_ext='json')
    blue_team_name = blue_features.filename
    for cls_type in blue_team[1:]:
        blue_member = cls_type()
        blue_member.load(blue_member.output_filename, file_ext='json')
        blue_features['features'].extend(blue_member['features'])
        blue_team_name += '_' + blue_member.filename

    cls_red_leader = red_team[0]
    red_features = cls_red_leader()
    red_features.load(red_features.output_filename, file_ext='json')
    red_team_name = red_features.filename
    for cls_type in red_team[1:]:
        red_member = cls_type()
        red_member.load(red_member.output_filename, file_ext='json')
        red_features['features'].extend(red_member['features'])
        red_team_name += '_' + red_member.filename

    return blue_features, blue_team_name, red_features, red_team_name


def team_conflict(blue_team: list, red_team: list) -> None:
    if not blue_team or not red_team:
        return None

    blue_features, blue_team_name, red_features, red_team_name = create_teams(blue_team, red_team)

    blue_features['COPYRIGHT'] = 'The data is made available under ODbL.'
    for blue_feature in blue_features:
        cr_position = Position(blue_feature['geometry']['coordinates'])
        blue_feature['properties']['intensity'] = {'base': 0, 'day': 0, 'night': 0}

        calc_base = True
        calc_day = int(blue_feature['properties'].get('Lampe - Température Couleur') or '5000') > 2500 and \
            blue_feature['properties'].get('Lampe - Régime (simplifié)') != "Détéction en milieu de nuit"
        calc_night = blue_feature['properties'].get('Lampe - Régime (simplifié)') != "Abaissement en milieu de nuit"

        for red_feature in red_features:
            geo_distance_between = cr_position.distance(red_feature['geometry']['coordinates'])
            diff_lum_tree_height = max(int(blue_feature['properties'].get("Lampe - Hauteur de feu", "10")) - 5, 0)
            square_distance = diff_lum_tree_height ** 2 + geo_distance_between ** 2
            if square_distance <= 25 ** 2:
                item_intensity = blue_feature['properties']['intensity']
                # valeur multipliée par 9 pour avoir des valeurs comprises entre 0 et 1
                # TODO: à revoir
                intensity_value = 9 / square_distance
                if calc_base:
                    item_intensity['base'] += intensity_value
                    if calc_day:
                        item_intensity['day'] += intensity_value
                        if calc_night:
                            item_intensity['night'] += intensity_value

    blue_features.dump('conflict_' + blue_team_name + '__' + red_team_name + '.json')


def team_contradiction(blue_team: list, red_team: list) -> None:
    if not blue_team or not red_team:
        return None

    blue_features, blue_team_name, red_features, red_team_name = create_teams(blue_team, red_team)
    new_geojson = Geojson(cpr='The data is made available under ODbL.')
    for blue_feature in blue_features:
        blue_position = Position(blue_feature['geometry']['coordinates'])
        calc_day = True
        calc_night = not blue_feature['properties'].get('opening_hours')

        for red_feature in red_features:
            red_position = red_feature['geometry']['coordinates']
            geo_distance_between = blue_position.distance(red_position)
            if geo_distance_between <= 25:
                item_intensity = {'day': 0, 'night': 0, 'diff': 0, }
                intensity_value = round(1 - (geo_distance_between**2)/(25**2), 2)
                if calc_day:
                    item_intensity['day'] += intensity_value
                    if calc_night:
                        item_intensity['night'] += intensity_value
                    item_intensity['diff'] = item_intensity['day'] - item_intensity['night']

                lat, lng = (blue_position + red_position)/2
                new_geojson.append({'intensity': item_intensity, 'lat': lat, 'lng': lng})

    new_works = Works()
    new_works.update(new_geojson)
    new_works.dump('conflict_' + blue_team_name + '__' + red_team_name + '.json')


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
        # team_conflict(blue_team=[Lamps], red_team=[Trees, Birds])
        # team_contradiction(blue_team=[Crossings, Shops], red_team=[Trees, Birds])
        app.run()
