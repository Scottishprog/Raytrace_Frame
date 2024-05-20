import time

import numpy as np
from messages import ToUiMessage
import time

world_list = {}
tree_view_list = []

# Sample reporting messaging code for slower renders:
# parent_thread.send_message_to_ui(ToUiMessage(f'Scanlines remaining: {height - i}', working_array))

def add_world(function):
    world_list[function.__name__] = function
    tree_view_list.append(["Graphical Hello World", f'3.3 {function.__name__}'])
    return function


@add_world
def hello_world(height, width, working_array, parent_thread):
    for i in range(0, height):
        for j in range(0, width):
            working_array[i, j, 0] = i / (height - 1)
            working_array[i, j, 1] = j / (width - 1)
            working_array[i, j, 2] = 0.0
    return working_array
