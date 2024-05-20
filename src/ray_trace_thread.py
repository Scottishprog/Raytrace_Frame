import threading
import numpy as np
from messages import ToUiMessage
import time
from worlds import (world_list)


class RayTraceThread(threading.Thread):
    def __init__(self, parent_thread):
        super().__init__()
        self.parent_thread = parent_thread
        self.thread = threading.Thread(target=self.run_thread)
        self.thread.start()

    def run_thread(self):
        start_message = self.parent_thread.from_ui_message_queue.get(block=True)
        self.parent_thread.from_ui_message_queue.task_done()
        # TODO add logic to actually look at the message run state, and act accordingly
        self.parent_thread.send_message_to_ui(ToUiMessage('Started'))
        print(f'Height: {start_message.height}, Width: {start_message.width}, world: {start_message.world}')

        working_array = np.ones((start_message.height, start_message.width, 3))
        print(f'Array format: {working_array.shape}')
        working_array = world_list[start_message.world](start_message.height,
                                                        start_message.width,
                                                        working_array,
                                                        self.parent_thread)

        # TODO during the running loop, push updates periodically, and listen for a stop command

        self.parent_thread.send_message_to_ui(ToUiMessage('Finished', working_array, True))
