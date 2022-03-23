var fileLayer = [
    {
        filename: 'conflict_lamps__trees.json',
        layername: 'Jour',
    },
    {
        filename: 'conflict_lamps_night__trees.json',
        layername: 'Nuit',
    },
]

new conflictHeatMap(fileLayer);

// basic leaflet traduction
document.getElementsByClassName('leaflet-control-zoom-in')[0].title = 'Zoom avant';
document.getElementsByClassName('leaflet-control-zoom-out')[0].title = 'Zoom arrière';