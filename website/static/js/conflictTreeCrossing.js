var fileLayer = {
    filename: 'conflict_crossings_shops__trees_birds.json',
    legendName: 'Contradiction',
    legendUnit: 'C',
    layers:
    [
        {
            layerName: 'Jour',
            layerType: 'heatmap',
            intensityKey: 'day',
        },
        {
            layerName: 'Nuit',
            layerType: 'heatmap',
            intensityKey: 'night',
        },
        {
            layerName: 'Différence',
            layerType: 'heatmap',
            intensityKey: 'diff',
        }
    ]}

new conflictHeatMap(fileLayer);

// basic leaflet traduction
document.getElementsByClassName('leaflet-control-zoom-in')[0].title = 'Zoom avant';
document.getElementsByClassName('leaflet-control-zoom-out')[0].title = 'Zoom arrière';
