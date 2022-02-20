from . import Osm_works
# (45.187501, 5.704696, 45.188848, 5.707703)


class Shops(Osm_works):
    filename = 'shops'
    query = \
        f"""
        (
            node[opening_hours][opening_hours!="24/7"]{Osm_works.BBOX};
        );
        """
