import numpy as np
from ray import (Ray, unit_vector)
from messages import ToUiMessage
import math
from hittable import (HittableObjectList, HitRecord)
from src.sphere import Sphere
from utility import (infinity, degrees_to_radians)
from sphere import Sphere

world_list = {}
tree_view_list = []


# Sample reporting messaging code for slower renders:
# parent_thread.send_message_to_ui(ToUiMessage(f'Scanlines remaining: {height - i}', working_array))

def my_add_world(data):
    def add_world(function):
        world_list[function.__name__] = function
        data[1] = data[1] + f'{function.__name__}'
        tree_view_list.append(data)
        return function

    return add_world


@my_add_world(["Graphical Hello World", '3.3 '])
def hello_world(height, width, working_array, parent_thread):
    for i in range(0, height):
        for j in range(0, width):
            working_array[i, j, 0] = i / (height - 1)
            working_array[i, j, 1] = j / (width - 1)
            working_array[i, j, 2] = 0.0
    return working_array


@my_add_world(["First Ray Trace", '4.2 '])
def first_raytrace(height, width, working_array, parent_thread):
    def ray_color(ray):
        unit_direction = unit_vector(ray.direction)
        a = 0.5 * (unit_direction[1] + 1.0)
        return (1.0 - a) * np.array([1.0, 1.0, 1.0]) + a * np.array([0.5, 0.7, 1.0])

    # Camera
    focal_length = 1.0
    viewport_height = 2.0
    viewport_width = viewport_height * (width / height)
    camera_center = np.array([0, 0, 0])

    # Calculate vectors on the vertical and horizontal viewport edges.
    viewport_u = np.array([viewport_width, 0, 0])
    viewport_v = np.array([0, -viewport_height, 0])
    print(f'viewport_u: {viewport_u}, viewport_v: {viewport_v}')

    # Calculate horizontal and vertical delta vectors from pixel to pixel
    pixel_delta_u = viewport_u / width
    pixel_delta_v = viewport_v / height
    print(f'pixel_delta_u: {pixel_delta_u}, pixel_delta_v: {pixel_delta_v}')

    # Calculate the upper left corner pixel location
    viewport_upper_left = camera_center - np.array([0, 0, focal_length]) - viewport_u / 2 - viewport_v / 2
    pixel00_loc = viewport_upper_left + .5 * (pixel_delta_u + pixel_delta_v)
    print(f'pixel00_loc: {pixel00_loc}, viewport_upper_left: {viewport_upper_left}')

    for i in range(0, height):
        parent_thread.send_message_to_ui(ToUiMessage(f'Scanlines remaining: {height - i}'))
        for j in range(0, width):
            pixel_center = pixel00_loc + (j * pixel_delta_u) + (i * pixel_delta_v)
            ray_direction = pixel_center - camera_center
            r = Ray(camera_center, ray_direction)

            color = ray_color(r)
            working_array[i, j] = color
    return working_array


@my_add_world(["Ray Trace w/ Sphere", '5.2 '])
def red_sphere(height, width, working_array, parent_thread):
    def hit_sphere(center, radius, ray):
        oc = center - ray.origin
        a = np.dot(ray.direction, ray.direction)
        b = -2.0 * np.dot(ray.direction, oc)
        c = np.dot(oc, oc) - radius * radius
        discriminant = b * b - 4 * a * c
        return discriminant >= 0

    def ray_color(ray):
        if hit_sphere(np.array([0, 0, -1]), 0.5, ray):
            return np.array([1, 0, 0])

        unit_direction = unit_vector(ray.direction)
        a = 0.5 * (unit_direction[1] + 1.0)
        return (1.0 - a) * np.array([1.0, 1.0, 1.0]) + a * np.array([0.5, 0.7, 1.0])

    # Camera
    focal_length = 1.0
    viewport_height = 2.0
    viewport_width = viewport_height * (width / height)
    camera_center = np.array([0, 0, 0])

    # Calculate vectors on the vertical and horizontal viewport edges.
    viewport_u = np.array([viewport_width, 0, 0])
    viewport_v = np.array([0, -viewport_height, 0])
    print(f'viewport_u: {viewport_u}, viewport_v: {viewport_v}')

    # Calculate horizontal and vertical delta vectors from pixel to pixel
    pixel_delta_u = viewport_u / width
    pixel_delta_v = viewport_v / height
    print(f'pixel_delta_u: {pixel_delta_u}, pixel_delta_v: {pixel_delta_v}')

    # Calculate the upper left corner pixel location
    viewport_upper_left = camera_center - np.array([0, 0, focal_length]) - viewport_u / 2 - viewport_v / 2
    pixel00_loc = viewport_upper_left + .5 * (pixel_delta_u + pixel_delta_v)
    print(f'pixel00_loc: {pixel00_loc}, viewport_upper_left: {viewport_upper_left}')

    for i in range(0, height):
        if i % 10 == 0:
            if i % 10 == 0:
                parent_thread.send_message_to_ui(ToUiMessage(f'Scanlines remaining: {height - i}', working_array))
        for j in range(0, width):
            pixel_center = pixel00_loc + (j * pixel_delta_u) + (i * pixel_delta_v)
            ray_direction = pixel_center - camera_center
            r = Ray(camera_center, ray_direction)

            color = ray_color(r)
            working_array[i, j] = color
    return working_array


@my_add_world(["Ray Trace w/ Surf. Norm.", '6.2 '])
def surface_norm(height, width, working_array, parent_thread):
    def hit_sphere(center, radius, ray):
        oc = center - ray.origin
        a = np.dot(ray.direction, ray.direction)
        h = np.dot(ray.direction, oc)
        c = np.dot(oc, oc) - radius * radius
        discriminant = h * h - a * c

        if discriminant < 0:
            return -1.0
        else:
            return (h - math.sqrt(discriminant)) / a

    def ray_color(ray):
        t = hit_sphere(np.array([0, 0, -1]), 0.5, ray)
        if t > 0:
            N = unit_vector(ray.at(t) - np.array([0, 0, -1]))
            return 0.5 * (1 + N)

        unit_direction = unit_vector(ray.direction)
        a = 0.5 * (unit_direction[1] + 1.0)
        return (1.0 - a) * np.array([1.0, 1.0, 1.0]) + a * np.array([0.5, 0.7, 1.0])

    # Camera
    focal_length = 1.0
    viewport_height = 2.0
    viewport_width = viewport_height * (width / height)
    camera_center = np.array([0, 0, 0])

    # Calculate vectors on the vertical and horizontal viewport edges.
    viewport_u = np.array([viewport_width, 0, 0])
    viewport_v = np.array([0, -viewport_height, 0])
    print(f'viewport_u: {viewport_u}, viewport_v: {viewport_v}')

    # Calculate horizontal and vertical delta vectors from pixel to pixel
    pixel_delta_u = viewport_u / width
    pixel_delta_v = viewport_v / height
    print(f'pixel_delta_u: {pixel_delta_u}, pixel_delta_v: {pixel_delta_v}')

    # Calculate the upper left corner pixel location
    viewport_upper_left = camera_center - np.array([0, 0, focal_length]) - viewport_u / 2 - viewport_v / 2
    pixel00_loc = viewport_upper_left + .5 * (pixel_delta_u + pixel_delta_v)
    print(f'pixel00_loc: {pixel00_loc}, viewport_upper_left: {viewport_upper_left}')

    for j in range(0, height):
        if j % 10 == 0:
            parent_thread.send_message_to_ui(ToUiMessage(f'Scanlines remaining: {height - j}', working_array))
        for i in range(0, width):
            pixel_center = pixel00_loc + (i * pixel_delta_u) + (j * pixel_delta_v)
            ray_direction = pixel_center - camera_center
            r = Ray(camera_center, ray_direction)

            color = ray_color(r)
            working_array[j, i] = color
    return working_array


@my_add_world(["Mult. Objects w/ Surf. Norm.", '6.7 '])
def mult_objects(height, width, working_array, parent_thread):
    def ray_color(ray, local_world: HittableObjectList):
        hit_record = HitRecord()
        if local_world.hit(ray, 0, infinity, hit_record):
            return 0.5 * (hit_record.normal + np.array([1, 1, 1]))

        unit_direction = unit_vector(ray.direction)
        a = 0.5 * (unit_direction[1] + 1.0)
        return (1.0 - a) * np.array([1.0, 1.0, 1.0]) + a * np.array([0.5, 0.7, 1.0])

    # World
    world = HittableObjectList()
    world.add(Sphere(np.array([0, 0, -1]), .05))
    world.add(Sphere(np.array([0, -100, -1]), 100))

    # Camera
    focal_length = 1.0
    viewport_height = 2.0
    viewport_width = viewport_height * (width / height)
    camera_center = np.array([0, 0, 0])

    # Calculate vectors on the vertical and horizontal viewport edges.
    viewport_u = np.array([viewport_width, 0, 0])
    viewport_v = np.array([0, -viewport_height, 0])
    print(f'viewport_u: {viewport_u}, viewport_v: {viewport_v}')

    # Calculate horizontal and vertical delta vectors from pixel to pixel
    pixel_delta_u = viewport_u / width
    pixel_delta_v = viewport_v / height
    print(f'pixel_delta_u: {pixel_delta_u}, pixel_delta_v: {pixel_delta_v}')

    # Calculate the upper left corner pixel location
    viewport_upper_left = camera_center - np.array([0, 0, focal_length]) - viewport_u / 2 - viewport_v / 2
    pixel00_loc = viewport_upper_left + .5 * (pixel_delta_u + pixel_delta_v)
    print(f'pixel00_loc: {pixel00_loc}, viewport_upper_left: {viewport_upper_left}')

    for j in range(0, height):
        if j % 10 == 0:
            parent_thread.send_message_to_ui(ToUiMessage(f'Scanlines remaining: {height - j}', working_array))
        for i in range(0, width):
            pixel_center = pixel00_loc + (i * pixel_delta_u) + (j * pixel_delta_v)
            ray_direction = pixel_center - camera_center
            r = Ray(camera_center, ray_direction)

            color = ray_color(r, world)
            working_array[j, i] = color
    return working_array
