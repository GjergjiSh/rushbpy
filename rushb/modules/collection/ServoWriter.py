import logging

from rushb.modules.RBModule import *
import datetime


class ServoWriter(RBModule):
    # Updates the servo values in the shared memory
    def __init__(self, **kwargs) -> None:
        self.left_val: int = kwargs.get("left_val")
        self.right_val: int = kwargs.get("right_val")
        self.top_val: int = kwargs.get("top_val")

    def init(self) -> None:
        logging.info("Initializing ServoWriter")

    def step(self, shared_mem: SharedMem) -> SharedMem:
        shared_mem.servo_vals.values[0] = self.left_val
        shared_mem.servo_vals.values[1] = self.right_val
        shared_mem.servo_vals.values[2] = self.top_val
        shared_mem.servo_vals.last_update = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        return shared_mem

    def deinit(self) -> None:
        logging.info("Deinitializing ServoWriter")
