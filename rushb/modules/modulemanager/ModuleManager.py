from rushb.modules.collection.IModuleInterface import *
from rushb.modules.factory.ModuleFactory import make_module

import os
import yaml
import logging

logging.basicConfig(
    level=logging.INFO,
    format="{asctime} {levelname:<8} {message}",
    style="{")

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
        except Exception as ex:

            print(ex)

    def deinit(self) -> None:
        """ Deinitialize all the assigned modules """
        try:
            for module in self.modules:
                module.deinit()
        except Exception as ex:
            print(ex)

    def run(self) -> None:
        """ Start processing the modules in a loop """
        try:
            while True:
                self.__step()
        except KeyboardInterrupt as ex:
            logging.info("Exiting...")

    def __read_config(self):
        """ Read the module configuration """
        with open(self.cfg_path, "r") as stream:
            try:
                yaml_file = yaml.safe_load(stream)
            except yaml.YAMLError as ex:
                print(ex)

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
        except Exception as ex:
            print(ex)
