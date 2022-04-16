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

    def _can_be_output(self, feature: Default_works.Model, bound=None, **kwargs) -> bool:
        bound = bound or self.bound
        if feature['geometry']:
            for lines in feature.position:
                try:
                    for position in lines:
                        if Position(position).in_bound(bound):
                            return True
                except TypeError:
                    break
        return False
