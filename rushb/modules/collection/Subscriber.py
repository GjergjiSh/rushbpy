import zmq
import logging

from rushb.modules.RBModule import *


class Subscriber(RBModule):
    """Subscriber is a class that subscribes to a ZMQ socket and writes the data to the shared memory"""

    def __init__(self, **kwargs) -> None:
        self.context = None
        self.socket = None
        self.port = kwargs.get("port")
        self.host = kwargs.get("host")

    def init(self) -> None:
        logging.info("Initializing Subscriber")
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.SUB)
        self.socket.connect(f"tcp://localhost:{self.port}")
        self.socket.setsockopt_string(zmq.SUBSCRIBE, "")

    def step(self) -> None:
        self.shared_mem = self.socket.recv_pyobj()

    def deinit(self) -> None:
        logging.info("Deinitializing Subscriber")
        self.socket.close()
