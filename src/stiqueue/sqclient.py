"""
This module implements a simple client for interacting with a message queue server.

Classes:
    SQClient: A client that connects to the message queue server to enqueue, dequeue, and check the count of messages.
"""

import socket
import sys
import time
import logging
import os


class SQClient:
    """
    A client that connects to a message queue server for enqueuing, dequeuing, and retrieving the count of messages.

    Attributes:
        host (str): The server's host address.
        port (int): The port number to connect to the server.
        socket (socket.socket): The client socket to communicate with the server.
        buff_size (int): Buffer size for sending and receiving messages.
        logger (logging.Logger): Logger for printing messages.
        ack_required (bool): Indicates whether an acknowledgment is required after the client receives the message.
    """

    def __init__(self, host="127.0.0.1", port=1234, logger=None, buff_size=None, ack_required=True):
        """
        Initializes the SQClient with the specified parameters.

        Args:
            host (str): The server's host address. Defaults to "127.0.0.1".
            port (int): The port number to connect to the server. Defaults to 1234.
            logger (logging.Logger, optional): Logger for logging messages. If None, a default logger is created.
            buff_size (int, optional): Buffer size for sending and receiving messages. Defaults to None.
            ack_required (bool): Indicates whether an acknowledgment is required after the client receives the message.
        """
        self.host = host
        self.port = port
        self.ack_required = ack_required
        if host is None:
            self.host = socket.gethostname()
        self.socket = None
        self.buff_size = buff_size
        if logger is None:
            logger = logging.getLogger(__name__)
            logger.setLevel(logging.DEBUG)
            ch = logging.StreamHandler()
            ch.setLevel(logging.DEBUG)
            logger.addHandler(ch)
        self.logger = logger

    def connect(self):
        """
        Establishes a connection to the messaging queue server.
        """
        self.logger.debug("Connecting to %s %d" % (self.host, self.port))
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if self.buff_size:
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, self.buff_size)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, self.buff_size)
        else:
            self.buff_size = self.socket.getsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF)
        self.socket.connect((self.host, self.port))

    def send_with_action(self, msg, action, recv=False):
        """
        Sends a message with a specified action to the server.

        Args:
            msg (bytes or str): The message to send. If not in bytes, it will be encoded.
            action (bytes): The action command (e.g., "enq", "deq", "cnt").
            recv (bool): Whether to expect a response from the server. Defaults to False.

        Returns:
            bytes: The server's response if recv is True, otherwise None.
        """
        total_ret_val = None
        if not isinstance(msg, bytes):
            msg = msg.encode()
        req = action+msg
        self.logger.debug("send with action: ")
        self.logger.debug(req)
        self.connect()
        self.socket.sendall(req)
        if recv:
            while True:
                ret_val = self.socket.recv(self.buff_size)
                self.logger.debug(f"DEBUGGING recv: <{ret_val}>")
                if total_ret_val is None:
                    total_ret_val = ret_val
                else:
                    total_ret_val += ret_val
                if ret_val in [b'', '']:
                    self.logger.debug(f"DEBUGGING: empty")
                    break
                elif ret_val is None:
                    self.logger.debug(f"DEBUGGING: time to break")
                    break
                elif len(ret_val) < self.buff_size:
                    self.logger.debug(f"DEBUGGING: ret val is smaller than buff size")
                    break

        self.disconnect()
        return total_ret_val

    def enq(self, msg):
        """
        Sends an "enqueue" request to the server.

        Args:
            msg (bytes or str): The message to enqueue. If not in bytes, it will be encoded.
        """
        self.send_with_action(msg, b"enq")

    def deq(self):
        """
        Sends a "dequeue" request to the server and receives the dequeued message.

        Returns:
            bytes: The dequeued message from the server.
        """
        msg = self.send_with_action(b"", b"deq", recv=True)
        if self.ack_required:
            self.ack()
        return msg

    def ack(self):
        """
        Sends an acknowledgement request to the server.

        """
        self.send_with_action(b"", b"ack")

    def cnt(self):
        """
        Sends a "count" request to the server and receives the count of messages in the queue.

        Returns:
            bytes: The count of messages in the queue.
        """
        return self.send_with_action(b"", b"cnt", recv=True)

    def peek(self, n=0, sep="\t"):
        """
        Sends a "count" request to the server and receives the count of messages in the queue.

        Returns:
            bytes: The count of messages in the queue.
        """
        if len(sep) != 1:
            raise Exception("The separator is expected to be a single character")
        return self.send_with_action(f"{sep}{n}".encode(), b"pek", recv=True)

    def disconnect(self):
        """
        Closes the connection to the server.
        """
        self.socket.close()


if __name__ == "__main__":
    print("CLIENT is STARTED> ...")
    host = "127.0.0.1"
    port = 1234
    if len(sys.argv) >= 2:
        host = sys.argv[1]
    if len(sys.argv) >= 3:
        port = int(sys.argv[2])

    local_logger = logging.getLogger(__name__)
    ch = logging.NullHandler()
    ch.setLevel(logging.INFO)
    local_logger.addHandler(ch)

    c = SQClient(host=host, port=port, logger=local_logger)
    for i in range(10):
        print(f"\n=========== {i} ==========")
        print(f"CLIENT> send num {i}")
        c.enq(b"num %d" % i)
        print("CLIENT> deq")
        v = c.deq()
        print(f"CLIENT: get num: {v}" )
