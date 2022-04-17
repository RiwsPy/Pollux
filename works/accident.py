from . import Default_works


class Works(Default_works):
    filename = "accidents_2019_2020"
    file_ext = "csv"
    COPYRIGHT_ORIGIN = 'www.data.gouv.fr'
    fake_request = True

    def _can_be_output(self, obj: Default_works.Model, **kwargs) -> bool:
        return super()._can_be_output(obj, **kwargs) and obj['properties']['lum'] in ('3', '4')

    class Model(Default_works.Model):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
