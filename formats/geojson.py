
class Geojson(dict):
    def __init__(self, cpr=''):
        super().__init__()
        self.type = "FeatureCollection"
        if cpr:
            self.COPYRIGHT = cpr
        self.features = []

    def __setattr__(self, key, value) -> None:
        self[key] = value

    def __getattr__(self, key):
        return self[key]

    def append(self, value) -> None:
        if type(value) is dict:
            try:
                value = Feature(**value)
            except ValueError:
                return
        self.features.append(value)

class Feature(dict):
    def __init__(self, *args, **kwargs):
        super().__setitem__('type', "Feature")
        if not kwargs or kwargs.get('geometry', {}).get('type') != 'Polygon':
            super().__setitem__('geometry', {'type': 'Point', 'coordinates': [0.0, 0.0]})
        else:
            super().__setitem__('geometry', kwargs['geometry'])
            del kwargs['geometry']
        super().__setitem__('properties', {})
        for k, v in kwargs.items():
            self[k] = v

    def __setattr__(self, key, value) -> None:
        self[key] = value

    def __getattr__(self, key):
        return self[key]

    def __setitem__(self, key, value):
        if key == 'properties':
            super().__setitem__(key, value)
        elif key in ('lat', 'Latitude'):
            self.geometry['coordinates'][1] = coord_pos_to_float(value)
        elif key in ('lng', 'long', 'lon', 'Longitude'):
            self.geometry['coordinates'][0] = coord_pos_to_float(value)
        else:
            self.properties.__setitem__(key, value)


def coord_pos_to_float(value) -> float:
    try:
        return float(value)
    except ValueError:
        if type(value) is str:
            return float(value.replace(',', '.'))
    raise ValueError


if __name__ == '__main__':
    g = Geojson()
    g.append({"id": 1, "lat": "48,7053500", "long": "4,7053500"})
    print(g)
