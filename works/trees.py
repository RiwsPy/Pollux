from . import Works
from api_ext.grenoble_alpes_metropole import Gam


class Trees(Works):
    filename = 'trees'
    request_method = Gam().call
    url = '/opendata/38185-GRE/EspacePublic/json/ARBRES_TERRITOIRE_VDG_EPSG4326.json'
    query = ""
    COPYRIGHT_ORIGIN = Gam.BASE_URL
    COPYRIGHT_LICENSE = 'ODbL'

    class Model(Works.Model):
        @property
        def id(self) -> int:
            return self.properties['ELEM_POINT_ID']

        @property
        def code(self) -> str:
            return self.properties['NOM']

        @property
        def taxon(self) -> str:
            # genus + species
            return self.properties['GENRE_BOTA'] + ' ' + self.properties['ESPECE']

        @property
        def planted_date(self) -> int:
            return int(self.properties.get('ANNEEDEPLANTATION', 0))

        @property
        def source(self) -> str:
            return 'local knowledge'

        @property
        def __dict__(self) -> dict:
            methods = ('id', 'code', 'taxon', 'planted_date', 'source')
            return {method: self[method] for method in methods}

        @property
        def height(self) -> int:
            return 5
