var fileLayer = {
    filename: 'conflict_lamps__trees_birds.json',
    layers:
    [
        {
            layerName: 'Sans filtre',
            intensityKey: 'base',
        },
        {
            layerName: 'Jour',
            intensityKey: 'day',
        },
        {
            layerName: 'Nuit',
            intensityKey: 'night',
        },
    ]}

new conflictHeatMap(fileLayer);

// basic leaflet traduction
document.getElementsByClassName('leaflet-control-zoom-in')[0].title = 'Zoom avant';
document.getElementsByClassName('leaflet-control-zoom-out')[0].title = 'Zoom arrière';