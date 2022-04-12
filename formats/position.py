from itertools import zip_longest
import math
from typing import List

EARTH_RADIUS = 6371000  # meters


class Position(List[float]):
    default_pos = 0.0

    @property
    def lat(self) -> float:
        return self[1]

    @property
    def lng(self) -> float:
        return self[0]

    def __add__(self, other) -> 'Position':
        return self.__class__([
            pos1+pos2
            for pos1, pos2 in zip_longest(self, other, fillvalue=self.default_pos)])
    __iadd__ = __add__

    def __truediv__(self, other: float) -> 'Position':
        return self.__class__([
            pos/other for pos in self]
        )

    def distance(self, other: List[float]) -> float:
        dlat_rad = math.radians(other[0]-self[0])
        dlon_rad = math.radians(other[1]-self[1])
        lat1_rad = math.radians(self[0])
        lat2_rad = math.radians(other[0])

        a = math.sin(dlat_rad/2)**2 + \
            math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon_rad/2)**2

        return EARTH_RADIUS * 2 * math.asin(a**0.5)

    def distance_from_way(self, other1: List[float], other2: List[float]) -> float:
        a1 = (other2[1] - other1[1]) / (other2[0] - other1[0])
        a2 = -1/a1
        b1 = other1[1] - a1*other1[0]
        b2 = self[1] - a2*self[0]
        x = (b2 - b1) / (a1 - a2)
        y = a1 * x + b1
        return self.distance([x, y])

    def in_bound(self, bound: List[float]) -> bool:
        lat_min, lng_min, lat_max, lng_max = bound
        return lat_min <= self.lat <= lat_max and lng_min <= self.lng <= lng_max


# [[Position], [Position], ...]
# TODO
class Relation:
    pass
