from typing import Callable

from .stage import Stage


class IfStage(Stage):
    def __init__(self, true_stage: Stage, false_stage: Stage, condition: Callable):
        self.true_stage = true_stage
        self.false_stage = false_stage
        self.condition = condition

    async def __call__(self, data):
        if self.condition(data):
            return await self.true_stage(data)

        return await self.false_stage(data)
