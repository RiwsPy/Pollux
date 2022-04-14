from formats.geojson import Geojson
from works import BASE_DIR, Default_works
import os
import json
from typing import List


class Works_cross:
    # Works_cross([teammate1, teammate2], [teammate1], [teammate1], ...)
    def __init__(self, *teams, bound: List[float] = None):
        bound = bound or Default_works.DEFAULT_BOUND
        self.teams = []
        self.copyrights = set()
        for team in teams:
            if not team:
                continue

            team_data = Geojson(name='')
            team_names = []
            team_cpr = set()
            for works_cls in team:
                team_works = works_cls.Works(bound=bound)
                team_works.load()
                new_features = team_works.bound_filter().features
                if new_features:
                    team_data.extend(new_features)
                    team_names.append(team_works.filename)
                    team_cpr.add(team_works.COPYRIGHT)
                    self.copyrights.add(team_works.COPYRIGHT)
            team_data.name = '&'.join(team_names)
            team_data.COPYRIGHT = ' -- '.join(team_cpr)
            self.teams.append(team_data)

    @property
    def db_name(self) -> str:
        return '|'.join(team.name for team in self.teams)

    @property
    def COPYRIGHT(self) -> str:
        return ' || '.join(self.copyrights)

    @property
    def features(self) -> list:
        ret = []
        for team in self.teams:
            ret.extend(team.features)
        return ret

    def dump(self, filename: str = "", features: list = None) -> None:
        print(f'db/cross/{filename or self.db_name + ".json"}')
        with open(os.path.join(BASE_DIR, f'db/cross/{filename or self.db_name + ".json"}'),
                  'w') as file:
            json.dump(Geojson(COPYRIGHT=self.COPYRIGHT, features=features or self.features),
                      file,
                      ensure_ascii=False,
                      indent=1)

    def apply_algo(self) -> None:
        pass
