from rushb.modules.RBModule import *
from rushb.modules.factory.ModuleFactory import make_module

import yaml
import logging


class ModuleManger:
    def __init__(self, cfg_path: str) -> None:
        self.modules: list[RBModule] = []
        self.cfg_path = cfg_path
        self.shared_mem = SharedMem()

    def init(self) -> bool:
        """ Parse the configuration file and initialize the modules """
        try:
            config = self.__read_config()
            self.__assign_modules(config)
            for module in self.modules:
                module.init()
        except RuntimeError:
            logging.critical("Module initialization failed", exc_info=True)
            return False

        return True

    def deinit(self) -> bool:
        """ Deinitialize all the assigned modules """
        try:
            for module in self.modules:
                module.deinit()
        except RuntimeError:
            logging.critical("Module deinitialization failed", exc_info=True)
            return False

        return True

    def run(self) -> bool:
        """ Start processing the modules in a loop """
        try:
            while True:
                self.__step()
        except KeyboardInterrupt:
            logging.info("Exiting...")
            return True
        except RuntimeError:
            logging.critical("Failed to run module", exc_info=True)
            return False

    def __read_config(self):
        """ Read the module parameters from the configuration file """
        with open(self.cfg_path, "r") as stream:
            yaml_file = yaml.safe_load(stream)
            return yaml_file

    def __assign_modules(self, config: dict):
        """ Assign a module to the manager """
        for module_name in config:
            module = make_module(module_name,**config[module_name])
            self.modules.append(module)

    def __step(self) -> None:
        """ Trigger the step function of all the assigned modules
            and update the shared memory """
        for module in self.modules:
            self.__push_sm(module)
            module.step()
            self.__pull_sm(module)

    def __push_sm(self, module: RBModule) -> None:
        """update the module's shared memory"""
        module.shared_mem = self.shared_mem

    def __pull_sm(self, module: RBModule) -> None:
        """update the manager's shared memory"""
        self.shared_mem = module.shared_mem
