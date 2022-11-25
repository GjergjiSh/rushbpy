from abc import ABC, abstractmethod

from rushb.sharedmem.SharedMem import SharedMem


class RBModule(ABC):
    @abstractmethod
    def init(self) -> None:
        raise NotImplementedError()

    @abstractmethod
    def step(self, shared_mem: SharedMem) -> SharedMem:
        raise NotImplementedError()

    @abstractmethod
    def deinit(self) -> None:
        raise NotImplementedError()
