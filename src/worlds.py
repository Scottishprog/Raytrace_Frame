import numpy as np


def hello_world(height, width):
    working_array = np.ones((height, width * 3))
    for i in range(0, height):
        for j in range(0, width * 3, 3):
            working_array[i, j] = i / (height - 1)
            working_array[i, j + 1] = (j // 3) / (width - 1)
            working_array[i, j + 2] = 0.0
    return working_array
