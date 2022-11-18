from abc import ABC, abstractmethod

from rushb.sharedmem.SharedMem import SharedMem


class RBModule(ABC):
    shared_mem = SharedMem()

    @abstractmethod
    def init(self) -> None:
        raise NotImplementedError()

    @abstractmethod
    def step(self) -> None:
        raise NotImplementedError()

    @abstractmethod
    def deinit(self) -> None:
        raise NotImplementedError()
