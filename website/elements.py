from ipyleaflet import Map, Marker, MarkerCluster, LayersControl, AwesomeIcon, FullScreenControl

def elements_map():
    icon1 = AwesomeIcon(
        name='tree',
        marker_color='green',
        icon_color='black',
        #spin=False
    )


    icon2 = AwesomeIcon(
        name='bus',
        marker_color='red',
        icon_color='black',
        #spin=False
    )

    icon3 = AwesomeIcon(
        name='building',
        marker_color='orange',
        icon_color='black',
        #spin=False
    )



    m = Map(center=(50, 0), zoom=5)

    marker1 = Marker(name='trees',icon=icon1, location=(48, -2))
    marker2 = Marker(name= 'trees', icon=icon1, location=(50, 0))
    marker3 = Marker(name = 'trees',icon=icon1, location=(52, 2))

    marker_cluster = MarkerCluster(
        markers=(marker1, marker2, marker3)
    )

    marker4 = Marker(name= 'bus',icon=icon2, location=(48, 3))
    marker5 = Marker(name= 'bus',icon=icon2, location=(50, 3.3))
    marker6 = Marker(name= 'bus',icon=icon2, location=(52, 3.5))

    marker_cluster_bus = MarkerCluster(
        markers=(marker4, marker5, marker6)
    )

    marker7 = Marker(name = 'building', icon=icon3, location=(48, 4))
    marker8 = Marker(name = 'building', icon=icon3, location=(50, 4.3))
    marker9 = Marker(name = 'building', icon=icon3, location=(52, 4.5))

    marker_cluster_building = MarkerCluster(
        markers=(marker7, marker8, marker9)
    )


    m.add_layer(marker_cluster);
    m.add_layer(marker_cluster_bus);
    m.add_layer(marker_cluster_building);

    control = LayersControl(position='topright')
    m.add_control(control)

    m.add_control(FullScreenControl())
    
    return m.save('website/templates/elements_map.html')
    