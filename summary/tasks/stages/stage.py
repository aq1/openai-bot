import abc
from typing import Generic, TypeVar

Inp = TypeVar('Inp')
Out = TypeVar('Out')


class Stage(abc.ABC, Generic[Inp, Out]):
    @abc.abstractmethod
    async def __call__(self, data: Inp) -> Out:
        ...
