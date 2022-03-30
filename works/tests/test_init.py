from .. import Works, convert_osm_to_geojson
import pytest
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent


def test_load():
    w = Works()
    w.load('empty')
    assert w['features'] == []
    with pytest.raises(KeyError):
        w['elements']

    w.file_ext = 'bad_ext'
    with pytest.raises(TypeError):
        w.load()


def test_iter():
    w = Works()
    w.load('empty')
    for feature1, feature2 in zip(w, w.features):
        assert feature1 == feature2


def test_convert_osm_to_geojson():
    w = Works()
    w.load('mock_osm')
    w2 = Works()
    w2.load('mock_geojson')
    assert convert_osm_to_geojson(w) == w2

    del w['features']
    with pytest.raises(KeyError):
        convert_osm_to_geojson(w)


def test_convert_osm_to_geojson_way():
    w = Works()
    w.load('mock_osm_way')
    w2 = Works()
    w2.load('mock_geojson_way')
    assert convert_osm_to_geojson(w) == w2


def test_can_be_output():
    w = Works()
    w.load('mock_geojson')
    for feature in w:
        assert w._can_be_output(feature)

    for feature in w:
        feature['geometry']['coordinates'] = [0.0, 0.0]
        assert not w._can_be_output(feature)


def test_fake_request():
    w = Works()
    w.fake_request = True
    w.load()
    assert w.request() == w
