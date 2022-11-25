import logging

from rushb.modules.RBModule import *


class ServoReader(RBModule):
    # ServoReader is a class that reads the servo values from the shared memory
    def __init__(self, **kwargs) -> None:
        pass

    def init(self) -> None:
        logging.info("Initializing ServoReader")

    def step(self, shared_mem: SharedMem) -> None:
        logging.debug(f"Servo values {shared_mem.servo_vals.values} {shared_mem.servo_vals.last_update}")
        return shared_mem

    def deinit(self) -> None:
        logging.info("Deinitializing ServoReader")
