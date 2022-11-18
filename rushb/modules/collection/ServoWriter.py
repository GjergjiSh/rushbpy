from rushb.modules.collection.IModuleInterface import *


class ServoReader(IModuleInterface):
    # ServoReader is a class that reads the servo values from the shared memory
    def __init__(self, **kwargs) -> None:
        self.message: str = kwargs.get("message")

    def init(self) -> None:
        print("Initializing")

    def step(self) -> None:
        print(self.shared_mem.servo_vals.values)
        print(self.shared_mem.servo_vals.last_update)

    def deinit(self) -> None:
        print("Deinit")
