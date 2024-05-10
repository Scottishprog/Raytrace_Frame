from tkinter import *
from tkinter import ttk
import queue
import numpy as np
from messages import from_ui_message


class Window:
    def __init__(self, root, width=800, height=600, title='Raytracing Frame'):
        self.__root = root
        self.__root.title(title)
        self.__width = width
        self.__height = height
        self.__array = None
        self.__image = None

        # Set up Message Queues to Ray_Trace_Thread
        self.from_ui_message_queue = queue.Queue()
        self.to_ui_message_queue = queue.Queue()
        self.to_ui_message_event = '<<to_ui_message>>'
        self.to_ui_array_event = '<<to_ui_array>>'
        self.__root.bind(self.to_ui_message_event, self.process_message)
        self.__root.bind(self.to_ui_array_event, self.process_array)

        # Set up Main Grid
        self.main_frame = ttk.Frame(self.__root, padding="3 3 3 12")
        self.main_frame.grid(row=0, column=0, sticky=(N, S, E, W))
        self.__root.columnconfigure(0, weight=1)
        self.__root.rowconfigure(0, weight=1)

        # Elements to be inserted into the main grid
        self.canvas = Canvas(self.main_frame, bg='white', width=width, height=height)
        self.canvas.grid(column=1, row=1, columnspan=4, sticky=N)

        self.canvas_x_val = StringVar()
        x_spinbox = ttk.Spinbox(self.main_frame, from_=200, to=2000, increment=50, width=8,
                                textvariable=self.canvas_x_val)
        x_spinbox.grid(column=2, row=2, sticky=W)
        self.canvas_x_val.set(f"{width}")

        self.canvas_y_val = StringVar()
        y_spinbox = ttk.Spinbox(self.main_frame, from_=200, to=2000, increment=50, width=8,
                                textvariable=self.canvas_y_val)
        y_spinbox.grid(column=4, row=2, sticky=W)
        self.canvas_y_val.set(f"{height}")

        ttk.Label(self.main_frame, text="Horizontal size: ").grid(column=1, row=2, sticky=E)
        ttk.Label(self.main_frame, text="Vertical size: ").grid(column=3, row=2, sticky=E)
        self.log_label = StringVar()
        ttk.Label(self.main_frame, textvariable=self.log_label).grid(column=5, row=3)

        ttk.Button(self.main_frame, text="Render", command=self.start_raytrace).grid(column=5, row=2)

        for child in self.main_frame.winfo_children():
            child.grid_configure(padx=5, pady=5)

    def start_raytrace(self):
        self.canvas.config(width=self.canvas_x_val.get(), height=self.canvas_y_val.get())
        start_message = from_ui_message(self.__height, self.__width, True)
        self.from_ui_message_queue.put(start_message)
        # TODO add additional code to actually do raytracing.

    def send_message_to_ui(self, message):
        self.to_ui_message_queue.put(message)
        self.__root.event_generate(self.to_ui_message_event, when='tail')

    def send_array_to_ui(self, array):
        self.to_ui_message_queue.put(array)
        self.__root.event_generate(self.to_ui_array_event, when='tail')

    def process_message(self, event):
        message = self.to_ui_message_queue.get(block=False)
        self.to_ui_message_queue.task_done()
        self.log_label.set(message)
        self.to_ui_message_queue.task_done()

    def process_array(self, event):
        # Pull the array from the queue
        self.__array = self.to_ui_message_queue.get(block=False)
        self.to_ui_message_queue.task_done()

        # Convert the array to PPM format image, so it can be sent to the canvas
        ppm_header = f'P6 {self.__width} {self.__height} 255 '.encode()
        data = ppm_header + self.__array.astype(np.uint8).tobytes()
        self.__image = PhotoImage(width=self.__width, height=self.__height, data=data, format='PPM')

        # Update Canvas
        self.canvas.delete('all')
        self.canvas.create_image(0, 0, anchor=NW, image=self.__image)


