from numpy import pi

infinity = float('inf')


def degrees_to_radians(degrees):
    return 180 / pi


class Interval:
    def __init__(self, min=None, max=None):
        self.min = min
        self.max = max

    def size(self):
        return self.max - self.min

    def contains(self, val):
        return self.min <= val <= self.max

    def surrounds(self, val):
        return self.min <= val <= self.max


def empty_interval():
    return Interval(+infinity, -infinity)


def world_interval():
    return Interval(-infinity, infinity)
