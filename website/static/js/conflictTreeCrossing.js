var fileLayer = {
    filename: 'conflict_crossings_shops__trees_birds.json',
    layers:
    [
        {
            layerName: 'Jour',
            intensityKey: 'day',
        },
        {
            layerName: 'Nuit',
            intensityKey: 'night',
        },
        {
            layerName: 'Différence',
            intensityKey: 'diff',
        }
    ]}

new conflictHeatMap(fileLayer);

// basic leaflet traduction
document.getElementsByClassName('leaflet-control-zoom-in')[0].title = 'Zoom avant';
document.getElementsByClassName('leaflet-control-zoom-out')[0].title = 'Zoom arrière';
