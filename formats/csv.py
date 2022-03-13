from .geojson import Geojson
import re
from typing import TextIO
import json

regex_csv_attr = re.compile('(?:^|,)(?=[^\"]|(\")?)\"?((?(1)[^\"]*|[^,\"]*))\"?(?=,|$)')


def convert_to_geojson(file: TextIO, regex=regex_csv_attr) -> dict:
    try:
        data = json.load(file)
    except TypeError:
        pass
    else:
        ret = Geojson()
        ret.update(data)
        return ret

    file_content = file.readlines()
    columns = file_content[0].partition('\n')[0]
    if columns[0] == '\ufeff':
        columns = columns[1:]

    columns = regex.findall(columns)

    ret = Geojson()
    for line in file_content[1:]:
        line = line.partition('\n')[0]
        line_data = {
            key[1]: value[1]
            for key, value in zip(columns, regex.findall(line))}
        ret.append(line_data)

    return ret