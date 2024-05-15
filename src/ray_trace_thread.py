import threading
import numpy as np
import messages
import time
from worlds import(hello_world)


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
        # TODO add to messages the ability of which world to run and act below accordingly.
        self.parent_thread.send_message_to_ui('Started!')
        print(f'Height: {start_message.height}, Width: {start_message.width}')

        working_array = hello_world(start_message.height, start_message.width)

        # TODO during the running loop, push updates periodically, and listen for a stop command

        working_array = (working_array * 255.99999).clip(0, 255)

        self.parent_thread.send_message_to_ui('Finished!')
        self.parent_thread.send_array_to_ui(working_array)
