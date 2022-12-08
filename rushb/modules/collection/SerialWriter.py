import serial
import logging
from io import TextIOWrapper, BufferedRWPair

from rushb.modules.RBModule import *
from rushb.sharedmem.SharedMem import ServoVals, Servos


class SerialWriter(RBModule):
    """SerialWriter is a class that writes the servo values to the serial port"""

    def __init__(self, **kwargs) -> None:
        self.serial_port = None
        self.sio = None
        self.port = kwargs.get("port")
        self.baudrate = kwargs.get("baudrate")

    def init(self) -> None:
        """Initialize the serial port"""
        logging.info("Initializing SerialWriter")

        # Check if the serial port name and baudrate are not None
        if self.port is None or self.baudrate is None:
            raise ValueError("The port and baudrate cannot be None")

        try:
            self.serial_port = serial.Serial(self.port, self.baudrate, timeout=1)
            self.sio: TextIOWrapper = TextIOWrapper(BufferedRWPair(self.serial_port, self.serial_port))
        except Exception as e:
            logging.error(f"Error while initializing the serial port: {e}")
            raise e

    def step(self, shared_mem: SharedMem) -> SharedMem:
        """Writes the servo values to the serial port"""
        servo_vals = SerialWriter.prep_servo_vals(shared_mem.servo_vals)
        logging.debug(f"Servo values to written to serial port {self.serial_port}: {servo_vals}")
        try:
            self.sio.write(servo_vals)
            self.sio.flush()
        except Exception as e:
            logging.error(f"Error while writing to the serial port: {e}")
            raise e

        return shared_mem

    def deinit(self) -> None:
        """Release the serial port"""
        logging.info("Deinitializing SerialWriter")
        try:
            # TODO FIXME
            #self.sio.close()
            self.serial_port.close()
        except Exception as e:
            logging.error(f"Error while deinitializing the serial port: {e}")
            raise e

    @staticmethod
    def prep_servo_vals(servo_vals: ServoVals) -> str:
        """Prepares the servo values for writing to the serial port"""
        return f"!{servo_vals.values[Servos.LEFT]}@{servo_vals.values[Servos.RIGHT]}#" \
               f"{servo_vals.values[Servos.CAMERA]}$\n"
