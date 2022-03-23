var fileLayer = [
    {
        filename: 'conflict_crossings_shops__trees.json',
        layername: 'Jour',
    },
    {
        filename: 'conflict_crossings__trees.json',
        layername: 'Nuit',
    },
    {
        filename: 'conflict_shops__trees.json',
        layername: 'Différence',
    }
]
new conflictHeatMap(fileLayer);

// basic leaflet traduction
document.getElementsByClassName('leaflet-control-zoom-in')[0].title = 'Zoom avant';
document.getElementsByClassName('leaflet-control-zoom-out')[0].title = 'Zoom arrière';
