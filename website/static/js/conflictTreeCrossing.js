var fileLayer = {
    filename: 'conflict_crossings_shops__trees_birds.json',
    legendName: 'Contradiction',
    layers:
    [
        {
            layerName: 'Jour',
            layerType: 'heatmap',
        },
        {
            layerName: 'Nuit',
            layerType: 'heatmap',
        },
        {
            layerName: 'Différence',
            layerType: 'heatmap',
        }
    ]}

new conflictHeatMap(fileLayer);
