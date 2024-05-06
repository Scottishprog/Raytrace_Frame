from tkinter import *
from tkinter import ttk


class Window:
    def __init__(self, root, width=800, height=600, title='Raytracing Frame'):
        self.__root = root
        self.__root.title(title)
        self.main_frame = ttk.Frame(self.__root, padding="3 3 12 12")
        self.main_frame.grid(row=0, column=0, sticky=(N, S, E, W))
        self.__root.columnconfigure(0, weight=1)
        self.__root.rowconfigure(0, weight=1)

        def calculate(*args):
            pass

        feet = StringVar()
        feet_entry = ttk.Entry(self.main_frame, width = 7, textvariable=feet)
        feet_entry.grid(column=2, row = 1, sticky=(W, E))

        meters = StringVar()
        ttk.Label(self.main_frame, textvariable=meters).grid(column=2, row = 2, sticky=(W, E))

        ttk.Button(self.main_frame, text="Calculate", command = calculate).grid(column=3, row=3, sticky=W)

        ttk.Label(self.main_frame, text="feet").grid(column = 3, row = 1, sticky = W)
        ttk.Label(self.main_frame, text="is equivalent to").grid(column=1, row=2, sticky=E)
        ttk.Label(self.main_frame, text="meters").grid(column=3, row=2, sticky=W)

        for child in self.main_frame.winfo_children():
            child.grid_configure(padx=5, pady=5)

        feet_entry.focus()

        #self.canvas = Canvas(self.__root, bg='black', width=width, height=height)
        #self.canvas.pack(fill=BOTH, expand=True)
        self.__is_running = False
        self.__root.protocol("WM_DELETE_WINDOW", self.close)

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self):
        self.__is_running = True
        while self.__is_running:
            self.redraw()
        print('Window has been closed')

    def close(self):
        self.__is_running = False

