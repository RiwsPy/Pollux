from .. import Works, convert_osm_to_geojson
import pytest


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
    print(w)
    print(w2)
    assert convert_osm_to_geojson(w) == w2

    del w['features']
    with pytest.raises(KeyError):
        convert_osm_to_geojson(w)
