from tkinter import *
from graphics import Window
from ray_trace_thread import RayTraceThread


def main():
    root = Tk()
    win = Window(root, 800, 600)
    ray_trace_thread = RayTraceThread(win)

    root.mainloop()

if __name__ == '__main__':
    main()
