import datetime

from rushb.modules.rb_module import *
from rushb.sharedmem.shared_mem import Servos


class ServoReader(RBModule):
    """The ServoReader reads and logs the servo values from the shared memory"""

    def __init__(self, **kwargs) -> None:
        pass

    def init(self) -> None:
        logging.info("Initializing ServoReader")

    def step(self, shared_mem: SharedMem) -> SharedMem:
        logging.debug(f"Servo values {shared_mem.servo_vals.values} {shared_mem.servo_vals.last_update}")
        return shared_mem

    def deinit(self) -> None:
        logging.info("Deinitializing ServoReader")


class ServoWriter(RBModule):
    """ The ServoWriter writes constant servo values to the shared memory """

    left_val: int
    right_val: int
    top_val: int

    def __init__(self, **kwargs) -> None:
        self.left_val: int = kwargs.get("left_val")
        self.right_val: int = kwargs.get("right_val")
        self.top_val: int = kwargs.get("top_val")

    def init(self) -> None:
        logging.info("Initializing ServoWriter")

    def step(self, shared_mem: SharedMem) -> SharedMem:
        shared_mem.servo_vals.values[Servos.LEFT] = self.left_val
        shared_mem.servo_vals.values[Servos.RIGHT] = self.right_val
        shared_mem.servo_vals.values[Servos.CAMERA] = self.top_val
        shared_mem.servo_vals.last_update = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        return shared_mem

    def deinit(self) -> None:
        logging.info("Deinitializing ServoWriter")
