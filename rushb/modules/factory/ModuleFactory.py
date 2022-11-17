from rushb.modules.collection.IModuleInterface import IModuleInterface
from rushb.modules.collection.TestModule import TestModule
from rushb.modules.collection.TestModuleDos import TestModuleDos

from abc import ABC, abstractmethod


class ModuleFactory(ABC):
    """ Base Factory that creates modules """
    @abstractmethod
    def create_module(self, **kwargs) -> IModuleInterface:
        pass


class TestModuleFactory(ModuleFactory):
    def create_module(self, **kwargs) -> IModuleInterface:
        """ Creates a test module """
        return TestModule(**kwargs)


class TestModuleFactoryDos(ModuleFactory):
    def create_module(self, **kwargs) -> IModuleInterface:
        """ Creates a test module dos  """
        return TestModuleDos(**kwargs)


def make_module(type : str, **kwargs) -> IModuleInterface:
    """ Create a module and assign parameters from the yml file """
    factories : dict[str,ModuleFactory] = {
        "TestModule" : TestModuleFactory(),
        "TestModuleDos" : TestModuleFactoryDos()
    }

    if type in factories:
        return factories[type].create_module(**kwargs)
    else:
        raise RuntimeError("Unsupported module type")


