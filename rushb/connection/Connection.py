import zmq
import logging

from enum import Enum
from rushb.sharedmem.SharedMem import *


class ConnectionType(Enum):
    PUB = "PUB"
    SUB = "SUB"
    PUBSUB = "PUBSUB"


class Connection:
    def __init__(self, **kwargs):
        self.connection_type: ConnectionType = ConnectionType[kwargs.get("connection_type")]
        self.pub_port: str = kwargs.get("pub_port")
        self.sub_port: str = kwargs.get("sub_port")
        self.sub_host: str = kwargs.get("sub_host")

        # Connection objects are not initialized until
        # the init_connection method is called
        self.context: zmq.Context = None
        self.publisher: zmq.Socket = None
        self.subscriber: zmq.Socket = None

    def __init_pub(self):
        # Init the publisher socket
        end_point = f"tcp://*:{self.pub_port}"
        self.publisher = self.context.socket(zmq.PUB)
        self.publisher.bind(end_point)
        logging.info(f"Publisher bound to {end_point}")

    def __init_sub(self):
        # Init the subscriber socket
        end_point = f"tcp://{self.sub_host}:{self.sub_port}"
        self.subscriber = self.context.socket(zmq.SUB)
        self.subscriber.connect(end_point)
        # Subscribe to all messages
        self.subscriber.setsockopt_string(zmq.SUBSCRIBE, "")
        logging.info(f"Subscriber connected to {end_point}")

    def init(self):
        # Init the context and the sockets based on the connection type
        self.context = zmq.Context()
        if self.connection_type == ConnectionType.PUB:
            self.__init_pub()
        elif self.connection_type == ConnectionType.SUB:
            self.__init_sub()
        elif self.connection_type == ConnectionType.PUBSUB:
            self.__init_pub()
            self.__init_sub()
        else:
            raise ValueError(f"Unknown connection type: {self.connection_type}")

    def send(self, shared_mem: SharedMem):
        # Try to send the shared memory to the remote subscriber
        self.publisher.send_pyobj(shared_mem)

    def recv(self) -> SharedMem:
        # Receive the shared memory from the remote publisher
        return self.subscriber.recv_pyobj()

    def deinit_connection(self):
        # Check if the publisher socket is initialized and close it
        if self.publisher is not None:
            self.publisher.close()

        # Check if the subscriber socket is initialized and close it
        if self.subscriber is not None:
            self.subscriber.close()

        # Check if the context is initialized and destroy it
        if self.context is not None:
            self.context.destroy()
