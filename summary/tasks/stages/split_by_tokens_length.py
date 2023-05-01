from typing import TypedDict

import tiktoken

from .stage import Stage


class In(TypedDict):
    content: str


class Out(TypedDict):
    total: int
    content: list[str]


class SplitByTokensLength(Stage[In, Out]):

    def __init__(self, max_tokens: int, max_parts: int):
        self.max_tokens = max_tokens
        self.max_parts = max_parts

    async def __call__(self, data: In) -> Out:
        encoding = tiktoken.get_encoding('cl100k_base')
        tokens = encoding.encode(data['content'])
        content = []
        for i in range(0, len(tokens), self.max_tokens):
            content.append(encoding.decode(tokens[i:i + self.max_tokens]))

        return {
            'total': len(tokens),
            'content': content[:self.max_parts],
        }
