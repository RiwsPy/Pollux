from . import Default_works
from api_ext.grenoble_alpes_metropole import Gam


class Works(Default_works):
    filename = 'trees'
    request_method = Gam().call
    url = '/opendata/38185-GRE/EspacePublic/json/ARBRES_TERRITOIRE_VDG_EPSG4326.json'
    query = ""
    COPYRIGHT_ORIGIN = Gam.BASE_URL
    COPYRIGHT_LICENSE = 'ODbL'

    class Model(Default_works.Model):
        @property
        def id(self) -> int:
            return self.properties['ELEM_POINT_ID']

        @property
        def code(self) -> str:
            return self.properties['NOM']

        @property
        def taxon(self) -> str:
            # genus + species
            return self.properties.get('GENRE_BOTA', '') + ' ' + self.properties.get('ESPECE', '')

        @property
        def planted_date(self) -> int:
            return int(self.properties.get('ANNEEDEPLANTATION', 0))

        @property
        def source(self) -> str:
            return 'local knowledge'

        @property
        def __dict__(self) -> dict:
            methods = ('id', 'code', 'taxon', 'planted_date')
            return {method: getattr(self, method, None) for method in methods}

        # TODO
        @property
        def height(self) -> int:
            return 5
