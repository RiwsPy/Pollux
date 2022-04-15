from . import Default_works
from api_ext.smmag import Smmag
from formats.position import Position


class Works(Default_works):
    filename = 'tc_ways'
    request_method = Smmag().call
    url = '/api/lines/json?types=ligne&reseaux=SEM'  # TODO: ajouter les trams ?
    query = ""
    COPYRIGHT_ORIGIN = Smmag.BASE_URL
    COPYRIGHT_LICENSE = 'ODbL'

    def _can_be_output(self, obj: Default_works.Model, bound=None, **kwargs) -> bool:
        bound = bound or self.bound
        if obj['geometry']:
            for lines in obj.position:
                for position in lines:
                    if Position(position).in_bound(bound):
                        return True
        return False
