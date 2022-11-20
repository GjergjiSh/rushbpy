import zmq
import logging

from rushb.sharedmem.SharedMem import *


class Publisher:
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

    def send(self, shared_mem: SharedMem) -> None:
        self.socket.send_pyobj(shared_mem)

    def deinit(self) -> None:
        logging.info("Deinitializing Publisher")
        self.socket.close()
        self.context.destroy()


class Subscriber:
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

    def recv(self) -> None:
        return self.socket.recv_pyobj()

    def deinit(self) -> None:
        logging.info("Deinitializing Subscriber")
        self.socket.close()
