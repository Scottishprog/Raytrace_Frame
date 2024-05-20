class FromUiMessage:
    def __init__(self, height, width, run=True, world=None):
        self.height = height
        self.width = width
        self.run = run
        self.world = world


class ToUiMessage:
    def __init__(self, message=None, array=None, stopped=False):
        self.stopped = stopped
        self.message = message
        self.array = array
