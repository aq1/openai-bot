from .stage import Stage


class Idle(Stage):
    async def __call__(self, data):
        return data
