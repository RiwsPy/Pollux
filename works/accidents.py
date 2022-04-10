from . import Works


class Accidents(Works):
    filename = "accidents_2019_2020"
    file_ext = "csv"
    COPYRIGHT_ORIGIN = 'www.data.gouv.fr'
    fake_request = True

    def _can_be_output(self, obj, bound=None) -> bool:
        return super()._can_be_output(obj) and obj['properties']['lum'] in ('3', '4')
