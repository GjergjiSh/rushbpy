from rushb.modules.collection.IModuleInterface import *
from rushb.modules.factory.ModuleFactory import make_module

import yaml
import logging

class ModuleManger():
    def __init__(self, cfg_path: str) -> None:
        self.modules: list[IModuleInterface] = []
        self.cfg_path = cfg_path

    def init(self) -> None:
        """ Initialize all the assigned modules """
        config = self.__read_config()
        self.__assign_modules(config)
        try:
            for module in self.modules:
                module.init()
        except Exception:
            logging.critical("", exc_info=True)

    def deinit(self) -> None:
        """ Deinitialize all the assigned modules """
        try:
            for module in self.modules:
                module.deinit()
        except Exception:
            logging.critical("", exc_info=True)

    def run(self) -> None:
        """ Start processing the modules in a loop """
        try:
            while True:
                self.__step()
        except KeyboardInterrupt:
            logging.info("Exiting...")

    def __read_config(self):
        """ Read the module configuration """
        try:
            with open(self.cfg_path, "r") as stream:
                yaml_file = yaml.safe_load(stream)
        except Exception:
            logging.critical("", exc_info=True)

        return yaml_file

    def __assign_modules(self, config : dict):
        """ Assign a module to the manager """
        for module_name in config:
            module = make_module(module_name,
                                 **config[module_name])
            self.modules.append(module)

    def __step(self) -> None:
        """ Trigger the step function of all the assigned modules """
        try:
            for module in self.modules:
                module.step()
        except Exception:
            logging.critical("", exc_info=True)
