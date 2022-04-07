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
        {
            layerName: 'Jour (arbre)',
            valueName: 'Jour',
            layerType: 'heatmap',
            filename: 'conflict_trees__lamps.json',
        },
        {
            layerName: 'Nuit (arbre)',
            valueName: 'Nuit',
            layerType: 'heatmap',
            filename: 'conflict_trees__lamps.json',
        },
        {
            layerName: 'Arbres',
            layerType: 'node',
            filename: 'conflict_trees__lamps.json',
            icon: 'markers/tree.png',
            entityType: 'Tree',
        },

    ]}

new conflictHeatMap(fileLayer, options={draw: false});
