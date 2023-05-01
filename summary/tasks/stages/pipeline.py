import typing

from .stage import Stage


class Pipeline(Stage):

    def __init__(self, stages: list[Stage]):
        self.stages = stages

    async def __call__(self, data):
        for stage in self.stages:
            data = await stage(data)
        return data
