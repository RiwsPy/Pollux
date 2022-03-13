from . import Works, BASE_DIR
import os
from formats.csv import convert_to_geojson


class Birds(Works):
    filename = "birds"
    file_ext = "csv"
    COPYRIGHT_ORIGIN = 'INPN-plateforme nationale du SINP'
    COPYRIGHT_LICENSE = 'etalab'

    def load(self, filename: str = '', file_ext: str = 'json') -> None:
        filename = filename or self.filename
        with open(os.path.join(BASE_DIR, f'db/{filename}.{file_ext or self.file_ext}'), 'r') as file:
            self.update(convert_to_geojson(file))
