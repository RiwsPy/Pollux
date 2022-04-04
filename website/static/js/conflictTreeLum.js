var fileLayer = {
    filename: 'conflict_lamps__trees_birds.json',
    legendName: 'Impact',
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
            layerName: 'Luminaires',
            layerType: 'node',
            filename: '.json',
            icon: 'marker_lamp.png',
            entityType: 'Lamp',
        },
    ]}

new conflictHeatMap(fileLayer);

// basic leaflet traduction
document.getElementsByClassName('leaflet-control-zoom-in')[0].title = 'Zoom avant';
document.getElementsByClassName('leaflet-control-zoom-out')[0].title = 'Zoom arrière';