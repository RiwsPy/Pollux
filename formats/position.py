from itertools import zip_longest
import math
from typing import List

EARTH_RADIUS = 6371000  # meters


class Position(List[float]):
    default_pos = 0.0

    def __init__(self, value: list = None):
        list.__setitem__(self, slice(None), value or [self.default_pos, self.default_pos])

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

    def force_position(self) -> 'Position':
        if type(self[0]) is list:
            return Relation(self).to_position()
        return self

    def distance(self, other: List[float]) -> float:
        my_pos = self.force_position()
        dlat_rad = math.radians(other[0]-my_pos[0])
        dlon_rad = math.radians(other[1]-my_pos[1])
        lat1_rad = math.radians(my_pos[0])
        lat2_rad = math.radians(other[0])

        a = math.sin(dlat_rad/2)**2 + \
            math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon_rad/2)**2

        return EARTH_RADIUS * 2 * math.asin(a**0.5)

    def distance_from_way(self, other1: List[float], other2: List[float]) -> float:
        my_pos = self.force_position()
        a1 = (other2[1] - other1[1]) / (other2[0] - other1[0])
        a2 = -1/a1
        b1 = other1[1] - a1*other1[0]
        b2 = my_pos[1] - a2*my_pos[0]
        x = (b2 - b1) / (a1 - a2)
        y = a1 * x + b1
        return self.distance([x, y])

    def in_bound(self, bound: List[float]) -> bool:
        if type(self[0]) is float:
            lat_min, lng_min, lat_max, lng_max = bound
            return lat_min <= self.lat <= lat_max and lng_min <= self.lng <= lng_max
        return Relation(self).in_bound(bound)

    def round(self, number=None) -> 'Position':
        if type(self[0]) is float:
            return self.__class__([round(ax, number) for ax in self])
        return self


# [[Position], [Position], ...]
# TODO
class Relation(list):
    default_pos = 0.0

    def __init__(self, value: list = None):
        list.__setitem__(self, slice(None), value or [[self.default_pos, self.default_pos]])

    @property
    def is_multiline(self) -> bool:
        return type(self[0][0]) is list

    def in_bound(self, bound: List[float]) -> bool:
        # TODO: surface
        if self.is_multiline:
            for lines in self:
                for position in lines:
                    if Position(position).in_bound(bound):
                        return True
        else:
            for position in self:
                if Position(position).in_bound(bound):
                    return True

        return False

    def to_position(self) -> Position:
        nb = 0
        cumul_lat = 0
        cumul_lng = 0
        if self.is_multiline:
            for positions in self:
                for position in positions:
                    cumul_lng += position[0]
                    cumul_lat += position[1]
                    nb += 1
        else:
            for position in self:
                cumul_lng += position[0]
                cumul_lat += position[1]
                nb += 1
        return Position([cumul_lng/nb, cumul_lat/nb])


LNG_1M = 1 / Position([0, 0]).distance([1, 0])
LAT_1M = 1 / Position([0, 0]).distance([0, 1])
