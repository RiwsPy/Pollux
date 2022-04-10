from . import Works, LNG_MAX, LNG_MIN, LAT_MIN, LAT_MAX


class Highways(Works):
    filename = 'highways'
    COPYRIGHT_LICENSE = 'ODbL'
    fake_request = True

    def _can_be_output(self, obj: dict, bound=None) -> bool:
        if obj['geometry']:
            for lines in obj['geometry']['coordinates']:
                if type(lines[0]) is list:
                    for obj_lng, obj_lat in lines:
                        if LAT_MIN <= obj_lat <= LAT_MAX and LNG_MIN <= obj_lng <= LNG_MAX:
                            return True
                else:
                    obj_lng, obj_lat = lines
                    if LAT_MIN <= obj_lat <= LAT_MAX and LNG_MIN <= obj_lng <= LNG_MAX:
                        return True
        return False
