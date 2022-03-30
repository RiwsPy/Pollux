import re
from pathlib import Path
import os
import json
from api_ext import Api_ext
from api_ext.osm import Osm
from typing import TextIO
from formats.geojson import Geojson
from formats.csv import convert_to_geojson

BASE_DIR = Path(__file__).resolve().parent.parent

LAT_MAX = 45.198848
LAT_MIN = 45.187501
LNG_MAX = 5.725703
LNG_MIN = 5.704696


class Works(dict):
    query = ""
    url = ""
    data_attr = "features"
    filename = "empty"
    file_ext = "json"
    request_method = Api_ext().call
    COPYRIGHT_ORIGIN = 'unknown'
    COPYRIGHT_LICENSE = 'unknown'
    fake_request = False  # no auto-request: request in local db

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

    def update(self, kwargs) -> None:
        super().update(convert_osm_to_geojson(kwargs))

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

    def output(self, filename: str = '') -> None:
        new_f = self.__class__()
        new_f.update(self)
        new_f[self.data_attr] = \
            [obj
             for obj in self
             if self._can_be_output(obj)]

        new_f.dump(filename=filename or self.output_filename + '.json')

    def _can_be_output(self, obj: dict) -> bool:
        obj_lng, obj_lat = obj['geometry']['coordinates']
        return LAT_MIN <= obj_lat <= LAT_MAX and LNG_MIN <= obj_lng <= LNG_MAX

    def dump(self, filename: str = '') -> None:
        with open(os.path.join(BASE_DIR, f'db/{filename or self.filename + ".json"}'), 'w') as file:
            json.dump({'COPYRIGHT': self.COPYRIGHT, **self}, file, ensure_ascii=False, indent=1)


class Osm_works(Works):
    request_method = Osm().call
    BBOX = f'({LAT_MIN}, {LNG_MIN}, {LAT_MAX}, {LNG_MAX})'
    skel_qt = False
    COPYRIGHT_ORIGIN = 'www.openstreetmap.org'
    COPYRIGHT_LICENSE = 'ODbL'

    def _can_be_output(self, obj) -> bool:
        return True

    def request(self, **kwargs) -> dict:
        return super().request(skel_qt=self.skel_qt, **kwargs)


convert_type = {'node': 'Point'}


def convert_osm_to_geojson(data_dict: dict) -> dict:
    if 'features' in data_dict:
        return data_dict
    if 'elements' not in data_dict:
        raise KeyError

    ret = Geojson(cpr=data_dict.get('COPYRIGHT', ''))

    for elt in data_dict['elements']:
        if elt.get('_dont_copy'):
            continue

        elt_geojson = dict()
        elt_geojson['type'] = "Feature"
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
                        elt_geojson['geometry']['coordinates'][0].append([data_node['lon'], data_node['lat']])
                        data_node['_dont_copy'] = True
                        break

        ret.append(elt_geojson)
    return ret


regex_csv_attr = re.compile('"+([^;.]*)"+')


def convert_csv_to_geojson(file: TextIO, regex=regex_csv_attr) -> dict:
    file_content = file.readlines()
    col_value0 = regex.findall(file_content[0])
    ret = Geojson()

    for line in file_content[1:]:
        if ';' in line:
            line_data = {
                key: value
                for key, value in zip(col_value0, regex.findall(line))}
            ret.append(line_data)

    return ret
