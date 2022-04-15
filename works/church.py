from . import Osm_works


class Works(Osm_works):
    filename = 'churchs'
    skel_qt = True
    query = \
        """
        area["name"="Grenoble-Alpes Métropole"]->.lim_area;
        
        (
          nwr(area.lim_area)[building=church];
          nwr(area.lim_area)[amenity=place_of_worship];
        );
        """
