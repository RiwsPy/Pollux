var fileLayer = {
    legendName: 'Contradiction',
    layers:
    [
        {
            layerName: 'Jour',
            layerType: 'heatmap',
            filename: 'crossings|lamps.json',
        },
        {
            layerName: 'Nuit',
            layerType: 'heatmap',
            filename: 'crossings|lamps.json',
        },
        {
            layerName: 'Luminaires',
            layerType: 'node',
            filename: 'lamps_output.json',
            icon: 'markers/lamp.png',
            entityType: 'Lamp',
        },
        {
            layerName: 'Passages piétons',
            layerType: 'node',
            filename: 'crossings|lamps.json',
            icon: 'markers/pedestrian.png',
            entityType: 'Crossing',
        },
    ]}

new conflictHeatMap(fileLayer, options={draw: false});
