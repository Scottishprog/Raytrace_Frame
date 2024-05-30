import numpy as np


def unit_vector(vector):
    norm = np.linalg.norm(vector)
    if norm == 0:
        return vector
    return vector / norm


class Ray:
    def __init__(self, origin, direction):  # Both inputs are size 3 vectors.
        self.origin = origin
        self.direction = direction

    def at(self, t):
        return self.origin + t * self.direction
