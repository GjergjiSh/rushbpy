import zmq
import logging

from enum import Enum
from rushb.sharedmem.shared_mem import *


class ConnectionType(Enum):
    PUBSUB = "PUBSUB"
    PUB = "PUB"
    SUB = "SUB"


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

    def init(self):
        """Initialize the connection"""
        # Check if the connection type is not None
        if self.connection_type is None:
            raise ValueError("The connection_type cannot be None")

        # Init the context
        try:
            self.context = zmq.Context()
        except zmq.error.ZMQError as e:
            logging.error(f"Could not init context: {e}")
            raise e

        # Init the publisher and subscriber sockets
        # depending on the connection type
        logging.info(f"Initializing connection of type {self.connection_type}")
        if self.connection_type == ConnectionType.PUB:
            self.init_pub()
        elif self.connection_type == ConnectionType.SUB:
            self.init_sub()
        elif self.connection_type == ConnectionType.PUBSUB:
            self.init_pub()
            self.init_sub()
        else:
            raise ValueError(f"Unknown connection type: {self.connection_type}")

    def send(self, shared_mem: SharedMem):
        """Send the shared memory to the remote subscriber"""
        try:
            self.publisher.send_pyobj(shared_mem)
        except zmq.error.ZMQError as e:
            logging.error(f"Could not send shared memory: {e}")
            raise e

    def recv(self) -> SharedMem:
        """Receive the shared memory from the remote publisher"""
        try:
            shared_mem = self.subscriber.recv_pyobj()
            return shared_mem
        except zmq.error.ZMQError as e:
            logging.error(f"Could not receive shared memory: {e}")
            raise e

    def deinit(self):
        try:
            # Check if the publisher socket is initialized and close it
            if self.publisher is not None:
                self.publisher.close()

            # Check if the subscriber socket is initialized and close it
            if self.subscriber is not None:
                self.subscriber.close()

            # Check if the context is initialized and destroy it
            if self.context is not None:
                self.context.destroy()
        except zmq.error.ZMQError as e:
            logging.error(f"Could not deinit connection: {e}")
            raise e

    def init_pub(self):
        # Check if the port is not None
        if self.pub_port is None:
            raise ValueError("The pub_port cannot be None")

        # Init the publisher socket
        end_point = f"tcp://*:{self.pub_port}"
        try:
            self.publisher = self.context.socket(zmq.PUB)
            self.publisher.bind(end_point)
            logging.info(f"Publisher bound to {end_point}")
        except zmq.error.ZMQError as e:
            logging.error(f"Could not bind the publisher to {end_point}: {e}")
            raise e

    def init_sub(self):
        # Check if the port and host are not None
        if self.sub_port is None:
            raise ValueError("The sub_port cannot be None")
        if self.sub_host is None:
            raise ValueError("The sub_host cannot be None")

        # Init the subscriber socket
        end_point = f"tcp://{self.sub_host}:{self.sub_port}"

        try:
            self.subscriber = self.context.socket(zmq.SUB)
            self.subscriber.connect(end_point)
            # Subscribe to all messages
            self.subscriber.setsockopt_string(zmq.SUBSCRIBE, "")
            logging.info(f"Subscriber connected to {end_point}")
        except zmq.error.ZMQError as e:
            logging.error(f"Could not connect to {end_point}: {e}")
            raise e
