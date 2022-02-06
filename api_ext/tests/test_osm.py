from ..osm import call
import requests
import pytest
from .. import BadStatusError
import os
import json
from . import BASE_DIR


class Mock_request:
    def __init__(self, status_code: int):
        self.status_code = status_code

    @staticmethod
    def json():
        with open(os.path.join(BASE_DIR, 'db/mock_osm.json'), 'r') as file:
            return json.load(file)


def test_call_ok(monkeypatch):
    def mock_get(*args, **kwargs):
        return Mock_request(200)

    monkeypatch.setattr(requests, "request", mock_get)
    req = call(0, query="")
    assert req['elements'] == [{
      "lat": 45.188724499762,
      "lon": 5.70497723253789,
      "type": "node",
      "tags": {
        "ELEM_POINT_ID": 22519,
        "CODE": "ESP28703"
      },
      "id": 2045858
    }]


def test_call_fail(monkeypatch):
    def mock_get(*args, **kwargs):
        return Mock_request(404)

    monkeypatch.setattr(requests, "request", mock_get)
    with pytest.raises(BadStatusError):
        call(0, query="")
