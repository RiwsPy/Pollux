from . import Works, BASE_DIR, convert_csv_to_geojson
import os


class Accidents(Works):
    filename = "accidents_caracteristiques_2020"
    file_ext = "csv"
    COPYRIGHT_ORIGIN = 'www.data.gouv.fr'

    def load(self, filename: str = '') -> None:
        filename = filename or self.filename
        with open(os.path.join(BASE_DIR, f'db/{filename}.{self.file_ext}'), 'r') as file:
            self.update(convert_csv_to_geojson(file))

    def _can_be_output(self, obj) -> bool:
        return super()._can_be_output(obj) and obj['properties']['lum'] in ('3', '4')
