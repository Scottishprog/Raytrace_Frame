from tkinter import *
from tkinter import ttk
import queue
import numpy as np
from messages import (FromUiMessage, ToUiMessage)
from ray_trace_thread import RayTraceThread
from worlds import (world_list, tree_view_list)


class Window:
    def __init__(self, root, width=800, height=600, title='Raytracing Frame'):
        self.__root = root
        self.__root.title(title)
        self.__width = width
        self.__height = height
        self.__array = None
        self.__image = None
        self.__canvas_updatable = True
        self.__root.protocol("WM_DELETE_WINDOW", self.on_exit)

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

        self.tv_frame = ttk.Frame(self.main_frame)
        self.tv_frame.grid(column=5, row=1, sticky=(N, E))
        self.tv = ttk.Treeview(self.tv_frame, columns=('1', '2'), height=29, selectmode='browse')
        self.tv.grid(column=1, row=1, sticky=E)

        self.sb = ttk.Scrollbar(self.tv_frame, orient='vertical', command=self.tv.yview)
        self.sb.grid(column=2, row=1, sticky=(N, W, S))
        self.tv.configure(yscrollcommand=self.sb.set)

        self.initialize_treeview(self.tv, tree_view_list)

        # Polishing and Presentation
        for child in self.main_frame.winfo_children():
            child.grid_configure(padx=5, pady=5)

    def on_exit(self):
        # TODO Add means of killing a running thread if needed.
        self.__root.destroy()

    def update(self):
        self.__canvas_updatable = True
        self.__root.after(500, self.update())

    def initialize_treeview(self, tv, data):
        self.tv.heading(1, text='Chapter')
        self.tv.heading(2, text='ID')
        self.tv.column("#0", width=300)
        self.tv.column(1, width=110, anchor='center')
        self.tv.column(2, width=150)

        for line in data:
            self.tv.insert('', 'end', text=line[0], values=line[1])

        # Set default selection at top
        default_id = self.tv.get_children()[0]
        self.tv.focus(default_id)
        self.tv.selection_set(default_id)

    def start_raytrace(self):

        # TODO disable the button until "stopped" message is received from thread.
        ray_trace_thread = RayTraceThread(self)
        self.canvas.config(width=self.canvas_x_val.get(), height=self.canvas_y_val.get())
        self.__width = int(self.canvas_x_val.get())
        self.__height = int(self.canvas_y_val.get())
        active_world = self.tv.item(self.tv.focus(), 'values')[1]

        start_message = FromUiMessage(self.__height, self.__width, True, active_world)
        self.from_ui_message_queue.put(start_message)

    def send_message_to_ui(self, message):
        self.to_ui_message_queue.put(message)
        self.__root.event_generate(self.to_ui_message_event, when='tail')

    def send_array_to_ui(self, array):
        self.to_ui_message_queue.put(array)
        self.__root.event_generate(self.to_ui_array_event, when='tail')

    def process_message(self, event):
        message = self.to_ui_message_queue.get(block=False)
        self.to_ui_message_queue.task_done()
        if message.stopped:
            pass
        if message.message is not None:
            self.log_label.set(message.message)
        if message.array is not None:
            self.__array = message.array
            self.process_array()

    def process_array(self):
        # Convert the array to PPM format image, so it can be sent to the canvas
        self.__array = (self.__array * 255.99999).clip(0, 255)
        ppm_header = f'P6 {self.__width} {self.__height} 255 '.encode()
        data = ppm_header + self.__array.astype(np.uint8).tobytes()
        self.__image = PhotoImage(width=self.__width, height=self.__height, data=data, format='PPM')

        # Update Canvas - if possible
        self.canvas.delete('all')
        self.canvas.create_image(0, 0, anchor=NW, image=self.__image)

        # TODO (unlikely) Update the UI code so it can handle faster update rates gracefully.
