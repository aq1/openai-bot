import abc
from typing import Generic, TypeVar

Inp = TypeVar('Inp')
Out = TypeVar('Out')


class StageException(BaseException):
    pass

class StopPipeline(StageException):
    pass


class Stage(abc.ABC, Generic[Inp, Out]):
    @abc.abstractmethod
    async def __call__(self, data: Inp) -> Out:
        ...
