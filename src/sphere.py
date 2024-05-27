from hittable import (HittableObject, HitRecord)
import numpy as np
import math


class Sphere(HittableObject):
    def __init__(self, center: np.array, radius):
        super().__init__()
        self.center = center
        self.radius = radius

    def hit(self, ray, ray_tmin, ray_tmax, hit_record: HitRecord):
        oc = self.center - ray.origin
        a = np.dot(ray.direction, ray.direction)
        h = np.dot(ray.direction, oc)
        c = np.dot(oc, oc) - self.radius * self.radius
        discriminant = h * h - a * c

        if discriminant < 0:
            return False

        sqrt_d = math.sqrt(discriminant)

        # Find the nearest root that lies in the acceptable range.
        root = (h - sqrt_d) / a
        if root <= ray_tmin or ray_tmax <= root:
            root = (h + sqrt_d) / a
            if root <= ray_tmin or ray_tmax <= root:
                return False

        hit_record.t = root
        hit_record.point = ray.at(hit_record.t)
        outward_normal = (hit_record.point - self.center) / self.radius
        hit_record.set_face_normal(ray, outward_normal)

        return True
