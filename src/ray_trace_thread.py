import threading
import time


class RayTraceThread(threading.Thread):
    def __init__(self, parent_thread):
        super().__init__()
        self.parent_thread = parent_thread
        self.thread = threading.Thread(target=self.run_thread); self.thread.start()

    def run_thread(self):
        time.sleep(1)
        self.parent_thread.send_message_to_ui('Test Message')