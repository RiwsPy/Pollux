import os
import json
from pathlib import Path
from formats.position import Position

BASE_DIR = Path(__file__).resolve().parent.parent


class Geojson(dict):
    def __init__(self, **kwargs):
        super().__init__()
        self.type = "FeatureCollection"
        self.COPYRIGHT = ''
        self.features = []
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __setattr__(self, key, value) -> None:
        self[key] = value

    def __getattr__(self, key):
        return self[key]

    def append(self, value) -> None:
        if not isinstance(value, Geojson):
            if type(value) is dict:
                try:
                    value = Geo_Feature(**value)
                except ValueError:
                    return
        self.features.append(value)

    def extend(self, features: list) -> None:
        for feature in features:
            self.append(feature)

    def dump(self, filename: str) -> None:
        with open(os.path.join(BASE_DIR, filename), 'w') as file:
            json.dump({'COPYRIGHT': self.COPYRIGHT, **self},
                      file,
                      ensure_ascii=False,
                      indent=1)


class Geo_Feature(dict):
    def __init__(self, *args, **kwargs):
        super().__setitem__('type', "Feature")
        if not kwargs or not kwargs.get('geometry'):
            super().__setitem__('geometry', {'type': 'Point', 'coordinates': None})
        else:
            super().__setitem__('geometry', kwargs['geometry'])
            del kwargs['geometry']

        self.position = self['geometry']['coordinates']

        super().__setitem__('properties', {})
        for k, v in kwargs.items():
            self[k] = v
        self["geometry"]['type'] = self.type_of_pos()

    def type_of_pos(self) -> str:
        if type(self.position[0]) is list:
            if type(self.position[0][0]) is list:
                try:
                    test = self.position[0][1]
                except IndexError:
                    return 'Polygon'
                else:
                    return 'MultiLineString'
        return 'Point'

    def __setattr__(self, key, value) -> None:
        self[key] = value

    def __getattr__(self, key):
        if key not in ('properties', 'values', 'geometry'):
            return self['properties'][key]
        return self[key]

    def __setitem__(self, key, value):
        if key in ('properties', 'values'):
            super().__setitem__(key, value)
        elif key == 'position':
            self['geometry']['coordinates'] = Position(value)
        elif key in ('lat', 'Latitude'):
            self.geometry['coordinates'][1] = coord_pos_to_float(value)
        elif key in ('lng', 'long', 'lon', 'Longitude'):
            self.geometry['coordinates'][0] = coord_pos_to_float(value)
        else:
            self['properties'].__setitem__(key, value)

    @property
    def position(self) -> Position:
        return self["geometry"]["coordinates"]

    @position.setter
    def position(self, value) -> None:
        self['geometry']['coordinates'] = Position(value)
        self["geometry"]['type'] = self.type_of_pos()


def coord_pos_to_float(value) -> float:
    try:
        return float(value)
    except ValueError:
        if type(value) is str:
            return float(value.replace(',', '.'))
    raise ValueError
