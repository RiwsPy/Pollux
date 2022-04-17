from . import Works_cross
from works import church, vending_machine


class Cross(Works_cross):
    max_range = 5000
    multiplier = 100

    def __init__(self):
        super().__init__([church], [vending_machine])

    def dump(self, filename: str = "", features: list = None) -> None:
        super().dump(features=self.teams[0].features)

    def apply_algo(self):
        for blue_teammate, red_teammate, distance in self._iter_double_and_range():
            blue_teammate['properties'][self.value_attr]['Contradiction'] += self.multiplier / distance
