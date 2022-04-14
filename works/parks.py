from . import Osm_works
# (45.187501, 5.704696, 45.188848, 5.707703)


class Works(Osm_works):
    filename = 'parks'
    query = \
        f"""
        (
            way[leisure=park]{Osm_works().BBOX};
        );
        """
    skel_qt = True
