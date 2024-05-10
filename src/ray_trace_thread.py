import threading
import numpy as np
import messages
import time



class RayTraceThread(threading.Thread):
    def __init__(self, parent_thread):
        super().__init__()
        self.parent_thread = parent_thread
        self.thread = threading.Thread(target=self.run_thread)
        self.thread.start()

    def run_thread(self):
        start_message = self.parent_thread.from_ui_message_queue.get(block=True)
        self.parent_thread.from_ui_message_queue.task_done()
        self.parent_thread.send_message_to_ui('Started!')

        working_array = np.ones((start_message.height, start_message.width*3))
        for i in range(0, start_message.height):
            for j in range(0, start_message.width*3, 3):
                working_array[i,j] = i/(start_message.height-1)
                working_array[i,j+1] = (j//3)/(start_message.width-1)
                working_array[i,j+2] = 0.0

        working_array = (working_array * 255.99999).clip(0, 255)

        self.parent_thread.send_message_to_ui('Finished!')
        self.parent_thread.send_array_to_ui(working_array)