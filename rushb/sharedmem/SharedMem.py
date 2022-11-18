from dataclasses import dataclass
import pickle
import datetime


@dataclass
class ServoVals:
    # ServoVals is a class that holds the values for the servos
    # and the time that the values were last updated
    def __init__(self):
        self.values = [0, 0, 0]
        self.last_update = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")


class SharedMem:
    # SharedMem is a class that holds the shared memory
    def __init__(self) -> None:
        self.servo_vals = ServoVals()


if __name__ == "__main__":
    shared_mem = SharedMem()
    # Pickle the object
    sm = pickle.dumps(shared_mem)
    print(sm)

    # Unpickle the object
    sm = pickle.loads(sm)
    print(sm.message)
