class HitRecord:
    def __init__(self, point=None, vector=None, t=None):
        self.point = point
        self.vector = vector
        self.t = t


class HittableObject:
    def __init__(self):
        pass

    def hit(self, ray, ray_tmin, ray_tmax, hit_record):
        return False
