import os
from pathlib import Path
from importlib import import_module

file_maps = os.listdir(Path(__file__).resolve().parent)
file_maps.remove('__init__.py')


class Configs(dict):
    def load(self) -> None:
        self.clear()
        for file in sorted(file_maps):
            cls, _, ext = file.rpartition('.')
            if ext != 'py':
                continue

            parent_dir = os.path.dirname(__file__).rsplit('/', 1)[-1]
            a = import_module('website.' + parent_dir + '.' + cls).Config()
            self[str(a.ID)] = a.__dict__


class Default_Config:
    ID = 0
    DEFAULT_DATA = {
        'template_name_or_list': 'maps/map.html',
        'mapJSMethod': 'create_map',
        'href': '',
        'description': {},
        'layers': [],
        'options': {}}

    DEFAULT_DESCRIPTION = {
        'href': '',
        'title': 'Titre par défaut',
        'accroche': 'Accroche par defaut',
        'intro': 'Introduction par défaut',
        'icon': '',
        'video': '',
        'QR': [],
    }

    @property
    def href(self) -> str:
        return self.DEFAULT_DATA.get('href', f'/map/{self.ID}')

    @property
    def __dict__(self) -> dict:
        ret = {**Default_Config.DEFAULT_DATA, **self.DEFAULT_DATA, **{'href': self.href}}
        ret['description'] = {**Default_Config.DEFAULT_DESCRIPTION, **ret['description']}
        return ret
