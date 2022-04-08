var fileLayer = {
    legendName: 'Impact',
    layers:
    [
        {
            layerName: 'Jour',
            layerType: 'heatmap',
            filename: 'lamps|trees.json',
        },
        {
            layerName: 'Nuit',
            layerType: 'heatmap',
            filename: 'lamps|trees.json',
        },
        {
            layerName: 'Luminaires',
            layerType: 'node',
            filename: 'lamps|trees.json',
            icon: 'markers/lamp.png',
            entityType: 'Lamp',
        },
        {
            layerName: 'Jour (arbre)',
            valueName: 'Jour',
            layerType: 'heatmap',
            filename: 'trees|lamps.json',
        },
        {
            layerName: 'Nuit (arbre)',
            valueName: 'Nuit',
            layerType: 'heatmap',
            filename: 'trees|lamps.json',
        },
        {
            layerName: 'Arbres',
            layerType: 'node',
            filename: 'trees|lamps.json',
            icon: 'markers/tree.png',
            entityType: 'Tree',
        },

    ]}

new conflictHeatMap(fileLayer, options={draw: false});
