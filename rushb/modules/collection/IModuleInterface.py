from abc import ABC, abstractmethod


class IModuleInterface(ABC):
    @abstractmethod
    def init(self) -> None:
        raise NotImplementedError()

    @abstractmethod
    def step(self) -> None:
        raise NotImplementedError()

    @abstractmethod
    def deinit(self) -> None:
        raise NotImplementedError()
