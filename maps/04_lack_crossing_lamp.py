from . import Default_Config


class Config(Default_Config):
    ID = "4"
    DATA = {
        'title': 'Eclairage des passages piétons',

        'options': {'draw': 0, 'legend': {
            'name': 'Manque'}},
        'layers': [
            {
                'layerName': 'Jour',
                'layerType': 'heatmap_intensity',
                'filename': 'cross/crossings|lamps.json',
            },
            {
                'layerName': 'Nuit',
                'layerType': 'heatmap_intensity',
                'filename': 'cross/crossings|lamps.json',
            },
            {
                'layerName': 'Luminaires',
                'layerType': 'cluster',
                'filename': 'lamps_output.json',
                'icon': 'markers/lamp.png',
                'entityType': 'Lamp',
            },
            {
                'layerName': 'Passages piétons',
                'layerType': 'cluster',
                'filename': 'cross/crossings|lamps.json',
                'icon': 'markers/pedestrian.png',
                'entityType': 'Crossing',
            },
        ]}
