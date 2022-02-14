from . import Works, BASE_DIR
import os
import re
from typing import TextIO
from formats.geojson import Geojson


class Birds(Works):
    filename = "birds"
    file_ext = "csv"
    COPYRIGHT_ORIGIN = 'INPN-plateforme nationale du SINP'
    COPYRIGHT_LICENSE = 'etalab'

    def load(self, filename: str = '') -> None:
        filename = filename or self.filename
        with open(os.path.join(BASE_DIR, f'db/{filename}.{self.file_ext}'), 'r') as file:
            self.update(convert_csv_to_geojson(file))


regex_csv_attr = re.compile('(?:^|,)(?=[^\"]|(\")?)\"?((?(1)[^\"]*|[^,\"]*))\"?(?=,|$)')


def convert_csv_to_geojson(file: TextIO) -> dict:
    file_content = file.readlines()
    col_value0 = regex_csv_attr.findall(file_content[0])
    ret = Geojson()
    for line in file_content[1:]:
        line_data = {
            key[1]: value[1]
            for key, value in zip(col_value0, regex_csv_attr.findall(line))}
        ret.append(line_data)

    return ret
