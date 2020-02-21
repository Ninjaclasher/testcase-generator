from random import Random


class CustomGenerator:
    def __init__(self):
        self.random = Random()
        self.is_initialized = False

    def next(self):
        raise NotImplementedError()

    def initialize(self):
        if self.is_initialized:
            raise ValueError('Cannot initialize twice')
        self.is_initialized = True
