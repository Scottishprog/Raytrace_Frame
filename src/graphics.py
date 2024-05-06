from tkinter import Tk, BOTH, Canvas

class Window:
    def __init__(self, width=800, height=600, title='Raytracing Frame'):
        self.__root = Tk()
        self.__root.title(title)
        self.canvas = Canvas(self.__root, bg='black', width=width, height=height)
        self.canvas.pack(fill=BOTH, expand=True)
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

