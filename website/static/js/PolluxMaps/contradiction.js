var fileLayer = {
    legendName: 'Contradiction',
    layers:
    [
        {
            layerName: 'Jour',
            layerType: 'heatmap',
            filename: 'conflict_crossings_shops__trees_birds.json',
        },
        {
            layerName: 'Nuit',
            layerType: 'heatmap',
            filename: 'conflict_crossings_shops__trees_birds.json',
        },
        {
            layerName: 'Différence',
            layerType: 'heatmap',
            filename: 'conflict_crossings_shops__trees_birds.json',
        }
    ]}

new conflictHeatMap(fileLayer, options={draw: false});
