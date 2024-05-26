from hittable import (HittableObject, HitRecord)

class Sphere (HittableObject):
    def __init__(self, center, radius):
        super(Sphere, self).__init__()
        self.center = center
        self.radius = radius

    def hit(self, ray, ray_tmin, ray_tmax, hit_record):
        pass

