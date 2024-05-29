from random import random
from hittable import (HitRecord, HittableObjectList)
from ray import (Ray, unit_vector)
from src.messages import ToUiMessage
from utility import (infinity, Interval)
import numpy as np


class Camera:
    def __init__(self, world, height, width, parent_thread):
        self.world = world
        self.height = height
        self.width = width
        self.parent_thread = parent_thread
        self.camera_center = None
        self.pixel00_loc = None
        self.pixel_delta_u = None
        self.pixel_delta_v = None

        self.initialize()

    def initialize(self):
        # Camera
        focal_length = 1.0
        viewport_height = 2.0
        viewport_width = viewport_height * (self.width / self.height)
        self.camera_center = np.array([0, 0, 0])

        # Calculate vectors on the vertical and horizontal viewport edges.
        viewport_u = np.array([viewport_width, 0, 0])
        viewport_v = np.array([0, -viewport_height, 0])
        print(f'viewport_u: {viewport_u}, viewport_v: {viewport_v}')

        # Calculate horizontal and vertical delta vectors from pixel to pixel
        self.pixel_delta_u = viewport_u / self.width
        self.pixel_delta_v = viewport_v / self.height
        print(f'pixel_delta_u: {self.pixel_delta_u}, pixel_delta_v: {self.pixel_delta_v}')

        # Calculate the upper left corner pixel location
        viewport_upper_left = self.camera_center - np.array([0, 0, focal_length]) - viewport_u / 2 - viewport_v / 2
        self.pixel00_loc = viewport_upper_left + .5 * (self.pixel_delta_u + self.pixel_delta_v)
        print(f'pixel00_loc: {self.pixel00_loc}, viewport_upper_left: {viewport_upper_left}')

    def sample_square(self):
        square_sample_point = np.array([random() - 0.5, random() - 0.5, 0])
        return square_sample_point

    def get_ray(self, i, j):
        # Construct a camera ray originating from the origin and directed at randomly sampled
        # point around the pixel location i, j.
        offset = self.sample_square()
        pixel_sample = self.pixel00_loc + ((i + offset[0]) * self.pixel_delta_u) + ((j+ + offset[1]) * self.pixel_delta_v)
        ray_origin = self.camera_center
        ray_direction = pixel_sample - ray_origin
        return Ray(ray_origin, ray_direction)

    def ray_color(self, ray: Ray, local_world: HittableObjectList):
        hit_record = HitRecord()
        if local_world.hit_interval(ray, Interval(0, infinity), hit_record):
            return 0.5 * (hit_record.normal + np.array([1, 1, 1]))

        unit_direction = unit_vector(ray.direction)
        a = 0.5 * (unit_direction[1] + 1.0)
        return (1.0 - a) * np.array([1.0, 1.0, 1.0]) + a * np.array([0.5, 0.7, 1.0])

    def render(self, working_array, samples_per_pixel=1, update_freq=10):
        pixel_samples_scale = 1.0/samples_per_pixel
        for j in range(0, self.height):
            if j % update_freq == 0:
                self.parent_thread.send_message_to_ui(ToUiMessage(
                    f'Scanlines remaining: {self.height - j}', working_array))
            for i in range(0, self.width):
                if samples_per_pixel > 1:
                    pixel_color = np.zeros(3)
                    for k in range(0, samples_per_pixel):
                        r = self.get_ray(i, j)
                        pixel_color += self.ray_color(r, self.world)
                    working_array[j, i] = pixel_color * pixel_samples_scale
                else:
                    pixel_center = self.pixel00_loc + (i * self.pixel_delta_u) + (j * self.pixel_delta_v)
                    ray_direction = pixel_center - self.camera_center
                    r = Ray(self.camera_center, ray_direction)
                    working_array[j,i] = self.ray_color(r, self.world)
        return working_array
