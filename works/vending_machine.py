from . import Osm_works


class Works(Osm_works):
    filename = 'vending_machine'
    query = \
        f"""
        area["name"="Grenoble-Alpes Métropole"]->.lim_area;
        (
            node(area.lim_area)[vending=condoms];
        );
        """