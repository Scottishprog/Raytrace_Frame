import numpy as np


class HitRecord:
    def __init__(self, point: np.array = None, normal=None, t=None, front_face=False):
        self.point = point
        self.normal = normal
        self.t = t
        self.front_face = front_face

    def set_face_normal(self, ray, outward_normal):
        # Sets the hit record normal vector.
        # NOTE: the parameter 'outward_normal' is assumed to have unit length.

        front_face = np.dot(ray.direction, outward_normal) < 0
        if front_face:
            self.normal = outward_normal
        else:
            self.normal = -outward_normal


class HittableObject:
    def __init__(self):
        pass

    def hit(self, ray, ray_tmin, ray_tmax, hit_record):
        return False


class HittableObjectList(HittableObject):
    def __init__(self):
        super().__init__()
        self.__objects = []

    def clear(self):
        self.__objects = []

    def add(self, hittable_object: HittableObject):
        self.__objects.append(hittable_object)

    def hit(self, ray, ray_tmin, ray_tmax, hit_record):
        temp_hit_record = HitRecord()
        hit_anything = False
        closest_so_far = ray_tmax
        for hittable_object in self.__objects:
            if hittable_object.hit(ray, ray_tmin, closest_so_far, hit_record):
                hit_anything = True
                closest_so_far = hit_record.t
                hit_record = temp_hit_record

        return hit_anything
