from rushb.modules.collection.IModuleInterface import *


class TestModuleDos(IModuleInterface):
    def __init__(self, **kwargs) -> None:
        self.message : str = kwargs.get("message")

    def init(self) -> None:
        print("Initializing")

    def step(self) -> None:
        print(f"Stepping {self.message}")

    def deinit(self) -> None:
        print("Deinit")
