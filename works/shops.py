from . import Osm_works


class Works(Osm_works):
    filename = 'shops'
    query = \
        f"""
        (
            node[opening_hours][opening_hours!="24/7"]{Osm_works().BBOX};
        );
        """
