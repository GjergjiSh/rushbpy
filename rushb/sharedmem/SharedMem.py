from dataclasses import dataclass
import datetime


@dataclass
class ServoVals:
    """"ServoVals is a class that holds the values for the servos
    and the time that the values were last updated"""
    def __init__(self):
        self.values = [90, 90, 90]
        self.last_update = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")


class SharedMem:
    """SharedMem is a class that holds the data shared between all modules"""
    def __init__(self) -> None:
        self.servo_vals = ServoVals()
        self.video_frame = None
