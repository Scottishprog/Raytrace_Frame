import time

import numpy as np
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


@my_add_world(["First Ray Trace", '4.1 '])
def first_raytrace(height, width, working_array, parent_thread):
    pass
