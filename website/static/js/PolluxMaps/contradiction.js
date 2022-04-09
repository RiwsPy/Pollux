var fileLayer = {
    legendName: 'Contradiction',
    layers:
    [
        {
            layerName: 'Jour',
            layerType: 'heatmap_intensity',
            filename: 'crossings&shops|trees.json',
        },
        {
            layerName: 'Nuit',
            layerType: 'heatmap_intensity',
            filename: 'crossings&shops|trees.json',
        },
        {
            layerName: 'Différence',
            layerType: 'heatmap_intensity',
            filename: 'crossings&shops|trees.json',
        }
    ]}

new conflictHeatMap(fileLayer, options={draw: false});
