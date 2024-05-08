from tkinter import *
from tkinter import ttk


class Window:
    def __init__(self, root, width=800, height=600, title='Raytracing Frame'):
        self.__root = root
        self.__root.title(title)
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
        self.canvas_x_val.set(f"{height}")

        self.canvas_y_val = StringVar()
        y_spinbox = ttk.Spinbox(self.main_frame, from_=200, to=2000, increment=50, width=8,
                                textvariable=self.canvas_y_val)
        y_spinbox.grid(column=4, row=2, sticky=W)
        self.canvas_y_val.set(f"{width}")

        ttk.Label(self.main_frame, text="Vertical size: ").grid(column=1, row=2, sticky=E)
        ttk.Label(self.main_frame, text="Horizontal size: ").grid(column=3, row=2, sticky=E)

        for child in self.main_frame.winfo_children():
            child.grid_configure(padx=5, pady=5)


