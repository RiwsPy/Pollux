from . import Osm_works


class Crossings(Osm_works):
    filename = 'crossings'
    query = \
        f"""
        (
            node[highway=crossing]{Osm_works.BBOX};
        );
        """
