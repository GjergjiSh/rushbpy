from abc import ABC, abstractmethod
from rushb.sharedmem.shared_mem import SharedMem

import importlib
import logging


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


def create_module(**kwargs) -> RBModule:
    """Create a module based on the module name and the kwargs"""

    # Get the module name
    module_name: str = kwargs.get("module_name")
    # Get the module class
    module_class: str = kwargs.get("module_class")

    # Check if the module name is None
    if module_name is None:
        raise ValueError("The module name cannot be None")

    # Check if the module class is None
    if module_class is None:
        raise ValueError("The module class cannot be None")

    # Import the module
    try:
        module = importlib.import_module(f"rushb.modules.collection.{module_name}")
        return getattr(module, module_class)(**kwargs)
    except ModuleNotFoundError as e:
        logging.error(f"Module {module_name}.{module_class} not found", exc_info=True)
        raise e
