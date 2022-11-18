from rushb.modules.collection.IModuleInterface import IModuleInterface
from rushb.modules.collection.ServoWriter import ServoReader
from rushb.modules.collection.ServoReader import ServoWriter

from abc import ABC, abstractmethod
import logging


class ModuleFactory(ABC):
    """ Base Factory that creates modules """
    @abstractmethod
    def create_module(self, **kwargs) -> IModuleInterface:
        pass


class TestModuleFactory(ModuleFactory):
    def create_module(self, **kwargs) -> IModuleInterface:
        """ Creates a test module """
        return ServoReader(**kwargs)


class TestModuleFactoryDos(ModuleFactory):
    def create_module(self, **kwargs) -> IModuleInterface:
        """ Creates a test module dos  """
        return ServoWriter(**kwargs)


def make_module(type: str, **kwargs) -> IModuleInterface:
    """ Create a module and assign parameters from the yml file """
    factories: dict[str, ModuleFactory] = {
        "ServoReader": TestModuleFactory(),
        "ServoWriter": TestModuleFactoryDos()
    }

    if type in factories:
        return factories[type].create_module(**kwargs)
    else:
        msg = "Unsupported module type"
        logging.critical(msg)
        raise ValueError(msg)
