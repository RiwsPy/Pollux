
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
        if not(type(value) is Geo_Feature):
            if type(value) is dict:
                try:
                    value = Geo_Feature(**value)
                except ValueError:
                    return
        self.features.append(value)

    def extend(self, data_list: list) -> None:
        self.features.extend(data_list)


class Geo_Feature(dict):
    def __init__(self, *args, **kwargs):
        super().__setitem__('type', "Feature")
        if not kwargs or kwargs.get('geometry', {}).get('type') != 'Polygon':
            super().__setitem__('geometry',
                                {'type': 'Point', 'coordinates': [0.0, 0.0]})
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
        elif key == 'values':
            super().__setitem__(key, value)
        else:
            self.properties.__setitem__(key, value)


def coord_pos_to_float(value) -> float:
    try:
        return float(value)
    except ValueError:
        if type(value) is str:
            return float(value.replace(',', '.'))
    raise ValueError
