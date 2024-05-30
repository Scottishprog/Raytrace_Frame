from numpy import pi
import numpy as np
from random import (random, uniform)
from ray import unit_vector

infinity = float('inf')


def degrees_to_radians(degrees):
    return degrees * pi/180.0


class Interval:
    def __init__(self, i_min=None, i_max=None):
        self.i_min = i_min
        self.i_max = i_max

    def size(self):
        return self.i_max - self.i_min

    def contains(self, val):
        return self.i_min <= val <= self.i_max

    def surrounds(self, val):
        return self.i_min <= val <= self.i_max


def empty_interval():
    return Interval(+infinity, -infinity)


def world_interval():
    return Interval(-infinity, infinity)


# For random number in [0,1) use random() for a range a,b use random(a,b)
def random_vector():
    return np.array([random(), random(), random()])


def random_vector_range(r_min, r_max):
    return np.array([uniform(r_min, r_max), uniform(r_min, r_max), uniform(r_min, r_max)])


def random_in_unit_sphere():
    while True:
        p = random_vector_range(-1, 1)
        if np.dot(p, p) < 1:
            return p


def random_unit_vector():
    return unit_vector(random_in_unit_sphere())


def random_on_hemisphere(normal: np.array):
    on_unit_sphere = random_unit_vector()
    if np.dot(on_unit_sphere, normal) > 0.0:
        return on_unit_sphere
    else:
        return -on_unit_sphere
