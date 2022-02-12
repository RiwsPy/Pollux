from .. import Works, convert_osm_to_geojson, convert_csv_to_geojson
import pytest
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent.parent


def test_load():
    w = Works()
    w.load('empty')
    assert w['features'] == []
    with pytest.raises(KeyError):
        w['elements']


def test_convert_osm_to_geojson():
    w = Works()
    w.load('mock_osm')
    w2 = Works()
    w2.load('mock_geojson')
    assert convert_osm_to_geojson(w) == w2

    del w['features']
    with pytest.raises(KeyError):
        convert_osm_to_geojson(w)


def test_convert_csv_to_geojson():
    with open(os.path.join(BASE_DIR, 'db/mock_csv.csv')) as file:
        assert convert_csv_to_geojson(file) == {
            'features': [{'geometry': {'coordinates': [0.0, 0.0], 'type': 'Point'},
                          'properties': {'Num_Acc': '202000000001', 'jour': '7'},
                          'type': 'Feature'}],
            'type': 'FeatureCollection'}
