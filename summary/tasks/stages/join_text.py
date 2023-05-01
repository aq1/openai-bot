from typing import TypedDict
from .stage import Stage


class In(TypedDict):
    content: list[str]


class Out(TypedDict):
    content: str


class JoinText(Stage[In, Out]):
    def __init__(self, symbol: str = ''):
        self.symbol = symbol

    async def __call__(self, data: In) -> Out:
        return {
            'content': self.symbol.join(data['content']),
        }
