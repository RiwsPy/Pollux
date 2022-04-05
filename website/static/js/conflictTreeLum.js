var fileLayer = {
    filename: 'conflict_lamps__trees_birds.json',
    legendName: 'Impact',
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
            layerName: 'Luminaires',
            layerType: 'node',
            filename: '.json',
            icon: 'markers/lamp.png',
            entityType: 'Lamp',
        },
    ]}

new conflictHeatMap(fileLayer);
