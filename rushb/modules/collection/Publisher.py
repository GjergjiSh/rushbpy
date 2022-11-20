import zmq
import logging

from rushb.modules.RBModule import *


class Publisher(RBModule):
    """Publisher is a class that publishes the data in the shared memory to a ZMQ socket"""

    def __init__(self, **kwargs) -> None:
        self.context = None
        self.socket = None
        self.port = kwargs.get("port")
        self.host = kwargs.get("host")

    def init(self) -> None:
        logging.info("Initializing Publisher")
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PUB)
        self.socket.bind(f"tcp://*:{self.port}")

    def step(self) -> None:
        self.socket.send_pyobj(self.shared_mem)

    def deinit(self) -> None:
        logging.info("Deinitializing Publisher")
        self.socket.close()
        self.context.destroy()
