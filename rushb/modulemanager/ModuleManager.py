from rushb.modules.RBModule import *
from rushb.modules.factory.ModuleFactory import make_module
from rushb.connection.Connection import *

import yaml
import logging


class ModuleManger:
    def __init__(self, cfg_path: str) -> None:
        self.cfg_path: str = cfg_path
        self.modules: list[RBModule] = []
        self.shared_mem: SharedMem = SharedMem()
        self.connection: Connection = None

    def init(self) -> bool:
        """ Parse the configuration file and initialize the modules """
        try:
            config = self.__read_config()
            self.__init_connection(config)
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
        try:
            with open(self.cfg_path, "r") as stream:
                logging.info("Reading configuration file")
                yaml_file = yaml.safe_load(stream)
                return yaml_file
        except FileNotFoundError:
            logging.critical("Configuration file not found", exc_info=True)

    def __assign_modules(self, config: dict):
        """ Assign a module to the manager """
        try:
            for module in config["Modules"]:
                # Get the module name to pass to the factory
                module_name = module["name"]
                # Remove the name from the dictionary to pass the
                # rest of the parameters to the module factory
                del module["name"]
                # Create and assign the module
                logging.info(f"Assigning module {module_name}")
                module = make_module(module_name, **module)
                self.modules.append(module)
        except RuntimeError:
            logging.critical("Module assignment failed", exc_info=True)

    def __step(self) -> None:
        """ Read the data from the connection process it and send it back """

        # Receive the shared memory from the remote publisher
        if self.connection.subscriber is not None:
            self.shared_mem = self.connection.recv()

        # Pass the shared memory to the modules and
        # trigger the step function
        for module in self.modules:
            self.__push_sm(module)
            module.step()
            self.__pull_sm(module)

        # Send the shared memory to the remote subscriber
        if self.connection.publisher is not None:
            self.connection.send(self.shared_mem)

    def __push_sm(self, module: RBModule) -> None:
        """update the module's shared memory"""
        module.shared_mem = self.shared_mem

    def __pull_sm(self, module: RBModule) -> None:
        """update the manager's shared memory"""
        self.shared_mem = module.shared_mem

    def __init_connection(self, config: dict) -> None:
        """ Initialize the publisher and subscriber """
        self.connection = Connection(**config["Connection"])
        try:
            self.connection.init()
        except RuntimeError:
            logging.critical("Connection initialization failed", exc_info=True)
