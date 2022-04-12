from pathlib import Path
import os
import json
from api_ext import Api_ext
from api_ext.osm import Osm
from formats.geojson import Geojson
from formats.csv import convert_to_geojson
from formats.position import Position
from typing import List

BASE_DIR = Path(__file__).resolve().parent.parent

LAT_MAX = 45.198848
LAT_MIN = 45.187501
LNG_MAX = 5.725703
LNG_MIN = 5.704696


class Default_works(dict):
    DEFAULT_BOUND = [LAT_MIN, LNG_MIN, LAT_MAX, LNG_MAX]
    query = ""
    url = ""
    data_attr = "features"
    filename = "empty"
    file_ext = "json"
    request_method = Api_ext().call
    COPYRIGHT_ORIGIN = 'unknown'
    COPYRIGHT_LICENSE = 'unknown'
    fake_request = False  # no auto-request: request in local db

    def __init__(self, *args, bound: List[float] = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.bound = bound

    def __iter__(self):
        yield from self.features

    @property
    def features(self) -> list:
        return self[self.data_attr]

    @property
    def COPYRIGHT(self) -> str:
        return f'The data included in this document is from {self.COPYRIGHT_ORIGIN}.' +\
               f' The data is made available under {self.COPYRIGHT_LICENSE}.'

    @property
    def output_filename(self) -> str:
        return self.filename + '_output'

    @property
    def bound(self) -> List[float]:
        return self._bound or self.DEFAULT_BOUND

    @bound.setter
    def bound(self, value: List[float]) -> None:
        self._bound = value

    def update(self, kwargs) -> None:
        super().update(convert_osm_to_geojson(kwargs))
        self[self.data_attr] = [self.Model(feature) for feature in self.features]

    def request(self, **kwargs) -> dict:
        if not self.fake_request:
            if self.query:
                kwargs['query'] = self.query

            return self.request_method(url=self.url, **kwargs)

        new_obj = self.__class__()
        new_obj.load()
        return new_obj

    def load(self, filename: str = '', file_ext: str = '') -> None:
        filename = filename or self.filename
        file_ext = file_ext or self.file_ext
        with open(os.path.join(BASE_DIR, f'db/{filename}.{file_ext}'), 'r') as file:
            if file_ext == 'json':
                file = json.load(file)
            elif file_ext == 'csv':
                file = convert_to_geojson(file)
            else:
                raise TypeError
            self.update(file)

    def bound_filter(self, bound: List[float] = None) -> 'Default_works':
        bound = bound or self.bound
        new_f = self.__class__(bound=bound)
        new_f.update(self)
        new_f[self.data_attr] = \
            [obj
             for obj in self
             if self._can_be_output(obj, bound=bound)]
        return new_f

    def output(self, filename: str = '') -> None:
        new_f = self.bound_filter(self.bound)
        new_f.dump(filename=filename or self.output_filename + '.json')

    def _can_be_output(self, obj: 'Default_works.Model', **kwargs) -> bool:
        return obj.position.in_bound(kwargs.get('bound', self.bound))

    def dump(self, filename: str = '') -> None:
        with open(os.path.join(BASE_DIR, f'db/{filename or self.filename + ".json"}'),
                  'w') as file:
            json.dump({'COPYRIGHT': self.COPYRIGHT, **self},
                      file,
                      ensure_ascii=False,
                      indent=1)

    class Model(dict):
        @property
        def properties(self) -> dict:
            return self.get('properties') or self.get('elements') or {}

        @property
        def position(self) -> Position:
            return Position(self['geometry']['coordinates'])

        @position.setter
        def position(self, value: List[float]) -> None:
            self['geometry']['coordinates'] = Position(value)


class Osm_works(Default_works):
    request_method = Osm().call
    skel_qt = False
    COPYRIGHT_ORIGIN = 'www.openstreetmap.org'
    COPYRIGHT_LICENSE = 'ODbL'

    def _can_be_output(self, obj, bound=None) -> bool:
        return True

    def request(self, **kwargs) -> dict:
        return super().request(skel_qt=self.skel_qt, **kwargs)

    @property
    def BBOX(self) -> str:
        return f'{tuple(self.bound)}'


convert_type = {'node': 'Point'}


def convert_osm_to_geojson(data_dict: dict) -> dict:
    if 'features' in data_dict:
        return data_dict
    if 'elements' not in data_dict:
        raise KeyError

    ret = Geojson(COPYRIGHT=data_dict.get('COPYRIGHT', ''))

    for elt in data_dict['elements']:
        if elt.get('_dont_copy'):
            continue

        elt_geojson = dict()
        elt_geojson['properties'] = elt.get('tags', {})
        if elt['type'] == 'node':
            elt_geojson['lat'] = elt['lat']
            elt_geojson['lng'] = elt['lon']
        elif elt['type'] == 'way':
            elt_geojson['geometry'] = {}
            elt_geojson['geometry']['type'] = 'Polygon'
            elt_geojson['geometry']['coordinates'] = [[]]
            for search_node_id in elt['nodes']:
                for data_node in data_dict['elements']:
                    if data_node['id'] == search_node_id:
                        elt_geojson['geometry']['coordinates'][0].append(
                            [data_node['lon'], data_node['lat']]
                        )
                        data_node['_dont_copy'] = True
                        break

        ret.append(elt_geojson)
    return ret
