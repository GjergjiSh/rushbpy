from rushb.modules.collection.IModuleInterface import *
import datetime


class ServoWriter(IModuleInterface):
    def __init__(self, **kwargs) -> None:

        self.left_val: int = kwargs.get("left_val")
        self.right_val: int = kwargs.get("right_val")
        self.top_val: int = kwargs.get("top_val")

    def init(self) -> None:
        print("Initializing")

    def step(self) -> None:
        self.shared_mem.servo_vals.values[0] = self.left_val
        self.shared_mem.servo_vals.values[1] = self.right_val
        self.shared_mem.servo_vals.values[2] = self.top_val
        self.shared_mem.servo_vals.last_update = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    def deinit(self) -> None:
        print("Deinit")
