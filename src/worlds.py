import time

import numpy as np
from ray import (Ray, unit_vector)
from messages import ToUiMessage
import time

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
        a = 0.5*(unit_direction[1] + 1.0)
        return (1.0 - a)*np.array([1.0, 1.0, 1.0]) + a*np.array([0.5, 0.7, 1.0])

    # Camera
    focal_length = 1.0
    viewport_height = 2.0
    viewport_width = viewport_height * (width/height)
    camera_center = np.array([0,0,0])

    # Calculate vectors on the vertical and horizontal viewport edges.
    viewport_u = np.array([viewport_width, 0, 0])
    viewport_v = np.array([0, -viewport_height, 0])
    print(f'viewport_u: {viewport_u}, viewport_v: {viewport_v}')

    # Calculate horizontal and vertical delta vectors from pixel to pixel
    pixel_delta_u = viewport_u / width
    pixel_delta_v = viewport_v / height
    print(f'pixel_delta_u: {pixel_delta_u}, pixel_delta_v: {pixel_delta_v}')

    # Calculate the upper left corner pixel location
    viewport_upper_left = camera_center - np.array([0,0, focal_length]) - viewport_u/2 - viewport_v/2
    pixel00_loc = viewport_upper_left + .5*(pixel_delta_u+pixel_delta_v)
    print(f'pixel00_loc: {pixel00_loc}, viewport_upper_left: {viewport_upper_left}')

    for i in range(0, height):
        for j in range(0, width):
            pixel_center = pixel00_loc + (i*pixel_delta_u) + (j*pixel_delta_v)
            ray_direction = pixel_center - camera_center
            r = Ray(camera_center, ray_direction)

            color = ray_color(r)
            working_array[i, j] = color
    return working_array

