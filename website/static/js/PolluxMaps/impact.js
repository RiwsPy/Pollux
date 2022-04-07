var fileLayer = {
    legendName: 'Impact',
    layers:
    [
        {
            layerName: 'Jour',
            layerType: 'heatmap',
            filename: 'conflict_lamps__trees_birds.json',
        },
        {
            layerName: 'Nuit',
            layerType: 'heatmap',
            filename: 'conflict_lamps__trees_birds.json',
        },
        {
            layerName: 'Luminaires',
            layerType: 'node',
            filename: 'conflict_lamps__trees_birds.json',
            icon: 'markers/lamp.png',
            entityType: 'Lamp',
        },
    ]}

new conflictHeatMap(fileLayer, options={draw: false, radius:10});
