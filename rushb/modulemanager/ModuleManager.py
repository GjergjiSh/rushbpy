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
            config = self.read_config()
            self.init_connection(config)
            self.assign_modules(config)
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
                self.update_shared_mem()
        except KeyboardInterrupt:
            logging.info("Exiting...")
            return True
        except RuntimeError:
            logging.critical("Failed to run module", exc_info=True)
            return False

    def read_config(self):
        """ Read the module parameters from the configuration file """
        try:
            with open(self.cfg_path, "r") as stream:
                logging.info("Reading configuration file")
                yaml_file = yaml.safe_load(stream)
                return yaml_file
        except FileNotFoundError:
            logging.critical("Configuration file not found", exc_info=True)

    def assign_modules(self, config: dict):
        """ Assign a module to the manager """
        try:
            for module in config["Modules"]:
                # Get the module name to pass to the factory
                if module["active"]:
                    module_name = module["name"]
                    # Create and assign the module
                    logging.info(f"Assigning module {module_name}")
                    module = make_module(module_name, **module)
                    self.modules.append(module)
        except RuntimeError:
            logging.critical("Module assignment failed", exc_info=True)

    def update_shared_mem(self) -> None:
        """ Read the data from the connection process it and send it back """

        # Receive the shared memory from the remote publisher
        if self.connection.subscriber is not None:
            self.shared_mem = self.connection.recv()

        # Pass the shared memory to the modules
        # and trigger the step function
        for module in self.modules:
            self.shared_mem = module.step(self.shared_mem)

        # Send the shared memory to the remote subscriber
        if self.connection.publisher is not None:
            self.connection.send(self.shared_mem)

    def init_connection(self, config: dict) -> None:
        """ Initialize the publisher and subscriber """
        self.connection = Connection(**config["Connection"])
        try:
            self.connection.init()
        except RuntimeError:
            logging.critical("Connection initialization failed", exc_info=True)
