from rushb.modules.RBModule import RBModule
from rushb.modules.collection.ServoWriter import ServoReader
from rushb.modules.collection.ServoReader import ServoWriter

from abc import ABC, abstractmethod


class ModuleFactory(ABC):
    """ Base Factory class for creating modules """
    @abstractmethod
    def create_module(self, **kwargs) -> RBModule:
        pass


class ServoReaderFactory(ModuleFactory):
    def create_module(self, **kwargs) -> RBModule:
        """ Create a ServoReader module """
        return ServoReader(**kwargs)


class ServoWriterFactory(ModuleFactory):
    def create_module(self, **kwargs) -> RBModule:
        """ Create a ServoWriter module """
        return ServoWriter(**kwargs)


def make_module(module_type: str, **kwargs) -> RBModule:
    """ Cre a module based on the module type and assign parameters """
    factories: dict[str, ModuleFactory] = {
        "ServoReader": ServoReaderFactory(),
        "ServoWriter": ServoWriterFactory()
    }

    if module_type in factories:
        return factories[module_type].create_module(**kwargs)
    else:
        raise ValueError("Unsupported module type")
