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
			logging.critical("Module initialization failed", exc_info=True)

	def deinit(self) -> None:
		""" Deinitialize all the assigned modules """
		try:
			for module in self.modules:
				module.deinit()
		except Exception:
			logging.critical("Module deinitialization failed", exc_info=True)

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
				return yaml_file
		except Exception:
			logging.critical("Failed to read the module configuration", exc_info=True)

	def __assign_modules(self, config: dict):
		""" Assign a module to the manager """
		try:
			for module_name in config:
				module = make_module(module_name,
								**config[module_name])
				self.modules.append(module)
		except Exception:
			logging.critical("Module assignment failed", exc_info=True)

	def __step(self) -> None:
		""" Trigger the step function of all the assigned modules """
		try:
			for module in self.modules:
				module.step()
		except Exception:
			logging.critical("Module step failed", exc_info=True)
