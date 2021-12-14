from abc import ABC


class BaseManager(ABC):
    """ Abstract class for handling common Manager operations. """

    def __init__(self, view, model=None):
        self.view = view
        self.model = model

    def start(self):
        """ Setup and launch the view in an infinite loop"""
        while True:
            self.view.setup(self)
            self.view.clear()
            self.view.start()
