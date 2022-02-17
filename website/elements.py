from ipyleaflet import Map, Marker, MarkerCluster, LayersControl, AwesomeIcon, FullScreenControl, LegendControl
import os
import json

def coord_files():
    '''
    Take the name and number of files 
    containing the 'output' string.
    To put in a list the coordinates from the docs *output.json 
    '''
    
    files_name = []
    count = 0

    path = "./db"
    for file in os.listdir(path):
        if 'output' in file:
            files_name.append(file)
            count += 1
    
    
    coordinates_={}
    for files in files_name:
        
        if not files in coordinates_:
            coordinates_[files] = []
            path2 = "./db/"+files
            f = open(path2)
            data = json.load(f)
            for i in data['features']:
                if 'coordinates' in i['geometry']:
                    coordinates_[files].append(i['geometry']['coordinates'])
  
                f.close()

            
    return coordinates_

def elements_map(coord_files:coord_files):   
    
    symbols ={'tc_ways_output.json':'subway', 'tc_stops_output.json':'bus', 'trees_output.json':'tree',
            'accidents_2019_2020_output.json':'stop-circle-o', 'parks_output.json':'car', 
              'crossings_output.json':'crosshairs'}


    colors = ['green',  'lightblue', 'blue', 'red', 'gray',   'purple',
             'lightgreen', 'darkblue',  'darkpurple', 'pink', 'orange', 
             'cadetblue','darkred',  'darkgreen', 'beige', 'lightgray', 'black', 'white']


    LAT_MAX = 45.188848
    LAT_MIN = 45.187501
    LNG_MAX = 5.707703
    LNG_MIN = 5.704696
    CENTER_LAT = LAT_MAX -(LAT_MAX-LAT_MIN)
    CENTER_LNG = LNG_MAX -(LNG_MAX-LNG_MIN)

    m = Map(center=(CENTER_LAT, CENTER_LNG), zoom=17)
    

    group_list = []
    legend_={}
    for val, keys in enumerate(coord_files().keys()):
        name = symbols[keys]
        marker_color = colors[val]
        icon_color='black'
        legend_[keys]=colors[val]
        
        
        markers_list = []
        for n in coord_files()[keys]:
            try:
                icon_ = AwesomeIcon(name=name, marker_color=marker_color, icon_color=icon_color)
                marks = Marker(name= name,
                               icon=icon_,
                               title = name,
                               location=(n[1],n[0]), 
                               draggable=False)

                markers_list.append(marks)
            except:
                pass

        marker_cluster = MarkerCluster(markers = markers_list)
        m.add_layer(marker_cluster);

    
    #control = LayersControl(position='topright')
    legend = LegendControl(legend_, name="Elements", position="bottomright")
    
    
    m.add_control(FullScreenControl())
    m.add_control(legend)
    #m.add_control(control)

#    return m


    return m.save('website/templates/elements_map.html', title='ele Map')

#elements_map(coord_files)
