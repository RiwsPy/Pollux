from . import Osm_works


class Lamps(Osm_works):
    filename = 'lamps'
    query = \
        f"""
        (
            node[highway=street_lamp]{Osm_works.BBOX};
        );
        """
