from . import Default_Config


class Config(Default_Config):
    ID = "church"
    DATA = {
        'title': 'Églises mal protégées',

        'options': {'draw': 0, 'radius': 100, 'legend': {
            'name': 'Églises protégées'}},
        'layers': [
            {
                'layerName': 'Contradiction',
                'layerType': 'heatmap_intensity',
                'filename': 'cross/churchs|vending_machine.json',
            },
            {
                'layerName': 'Églises',
                'layerType': 'node',
                'filename': 'cross/churchs|vending_machine.json',
            },
            {
                'layerName': 'Machines démoniaques',
                'layerType': 'node',
                'filename': 'vending_machine.json',
            },
        ]}
