var fileLayer = {
    legendName: 'Recommandations',
    layers: [
            {filename: 'trees_output.json',
             layerName: 'Arbres',
             layerType: 'node',
             entityType: 'Tree',
             icon: 'markers/tree.png'},

            {filename: 'crossings_output.json',
             layerName: 'Passages piétons',
             layerType: 'node',
             entityType: 'Crossing',
             icon: 'markers/pedestrian.png'},

            {filename: 'accidents_2019_2020_output.json',
             layerName: 'Accidents de voiture de nuit',
             layerType: 'node',
             entityType: 'Accident',
             icon: 'markers/accident.png'},

            {filename: 'tc_ways_output.json',
             layerName: 'Lignes de bus',
             layerType: 'node',
             entityType: 'BusLine'},

            {filename: 'tc_stops_output.json',
             layerName: 'Arrêts de transports en commun',
             layerType: 'node',
             entityType: 'PublicTransportStop',
             icon: 'markers/busstop.png'},

            {filename: 'parks_output.json',
             layerName: 'Parcs',
             layerType: 'node',
             entityType: 'Park'},

            {filename: 'birds_output.json',
             layerName: 'Observations oiseau',
             layerType: 'node',
             entityType: 'Animal',
             icon: 'markers/bird.png'},

            {filename: 'shops_output.json',
             layerName: 'Bâtiments accueillant du public',
             layerType: 'node',
             entityType: 'Shop',
             icon: 'markers/shop.png'},

            {filename: 'lamps_output.json',
             layerName: 'Luminaires',
             layerType: 'node',
             entityType: 'Lamp',
             icon: 'markers/lamp.png'},

            {filename: 'highways_output.json',
             layerName: 'Artères principales',
             layerType: 'node',
             entityType: 'Highway'},
          ]
}

new recommendationMap(fileLayer, options={legend: false});
