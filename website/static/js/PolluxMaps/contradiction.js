var fileLayer = {
    legendName: 'Contradiction',
    layers:
    [
        {
            layerName: 'Jour',
            layerType: 'heatmap',
            filename: 'crossings&shops|trees.json',
        },
        {
            layerName: 'Nuit',
            layerType: 'heatmap',
            filename: 'crossings&shops|trees.json',
        },
        {
            layerName: 'Différence',
            layerType: 'heatmap',
            filename: 'crossings&shops|trees.json',
        }
    ]}

new conflictHeatMap(fileLayer, options={draw: false});
