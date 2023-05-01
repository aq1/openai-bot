from .stage import Stage


class Idle(Stage):
    def __call__(self, data):
        return data
