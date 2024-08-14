"""
This module implements a simple message queue server.

Classes:
    SQServer: A server that handles enqueuing and dequeuing of messages.

Functions:
    cli: Command-line interface to start the server.
"""

import socket
from multiprocessing import Lock
import logging
import argparse


class SQServer:
    """
    A simple message queue server that listens for client connections and handing adding (enqueuing) and retrieving
    (dequeuing) of messages.

    Attributes:
        lock (Lock): A lock to synchronize access to the message queue.
        q (list): A list that acts as the message queue.
        action_len (int): Length of the action command in the message.
        socket (socket): The server socket for accepting connections.
        buff_size (int): Buffer size for sending and receiving messages.
        logger (logging.Logger): Logger for debugging and info messages.
        host (str): Host address of the server.
        port (int): Port number to bind the server.
        backlog (int): Maximum number of queued connections.
    """

    def __init__(self, host="127.0.0.1", port=1234, backlog=None, action_len=3, logger=None, buff_size=None):
        """
        Initializes the SQServer with the specified parameters.

        Args:
            host (str): The host address to bind the server. Defaults to "127.0.0.1".
            port (int): The port number to bind the server. Defaults to 1234.
            backlog (int, optional): Maximum number of queued connections. Defaults to None.
            action_len (int): Length of the action command in the message. Defaults to 3.
            logger (logging.Logger, optional): Logger for logging messages. If None, a default logger is created.
            buff_size (int, optional): Buffer size for sending and receiving messages. Defaults to None.
        """
        self.lock = Lock()
        self.q = []
        self.action_len = action_len
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if buff_size:
            self.buff_size = buff_size
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, buff_size)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, buff_size)
        else:
            self.buff_size = self.socket.getsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, self.buff_size)
        if not logger:
            logger = logging.getLogger(__name__)
            logger.setLevel(logging.INFO)
            ch = logging.StreamHandler()
            ch.setLevel(logging.INFO)
            logger.addHandler(ch)
        self.logger = logger
        if host is None:
            self.host = socket.gethostname()
            self.logger.debug("SERVER> self host: ")
            self.logger.debug(self.host)
        else:
            self.host = host

        self.port = port
        self.backlog = backlog
        self.socket.bind((self.host, self.port))
        self.logger.debug("SERVER> bounded to %s %d" % (self.host, self.port))

    def enq(self, msg):
        """
        Enqueues a message into the queue.

        Args:
            msg (bytes): The message to enqueue.
        """
        self.logger.debug("SERVER> enqueue: ")
        self.logger.debug(msg)
        self.lock.acquire()
        self.q.append(msg)
        self.lock.release()

    def deq(self, conn):
        """
        Dequeues a message from the queue and sends it to the client.

        Args:
            conn (socket): The client connection to send the message to.
        """
        self.lock.acquire()
        if len(self.q) > 0:
            v = self.q.pop(0)
            self.logger.debug("SERVER> dequeue: %s" % str(v))
            conn.sendall(v)
        self.lock.release()

    def cnt(self, conn):
        """
        Sends the count of messages in the queue to the client.

        Args:
            conn (socket): The client connection to send the count to.
        """
        b = b'%d' % len(self.q)
        conn.sendall(b)

    def listen(self):
        """
        Starts the server to listen for client connections continuously.
        """
        while True:
            self.listen_single()

    def other_actions(self, action_msg):
        """
        Handles other actions sent by the client.

        Args:
            action_msg (bytes): The message containing the action and its data.
        """
        self.logger.debug("SERVER> other action: " + str(action_msg))

    def listen_single(self):
        """
        Listens for a single client connection, processes the request, and closes the connection.
        """
        if self.backlog:
            self.socket.listen(self.backlog)
        else:
            self.socket.listen()
        self.logger.debug("SERVER> Waiting for client...")
        conn, addr = self.socket.accept()  # Accept connection when client connects
        self.logger.debug("SERVER> Connected by %s" % str(addr))
        action_msg = conn.recv(self.buff_size)  # Receive client data
        action = action_msg[:self.action_len]
        if len(action_msg) >= self.action_len:
            msg = action_msg[self.action_len:]
            if action == b"enq":
                self.enq(msg)
            elif action == b"deq":
                self.deq(conn)
            elif action == b"cnt":
                self.cnt(conn)
            else:
                self.logger.debug("SERVER> other action: ")
                self.logger.debug(action)
                self.other_actions(action_msg)
        else:
            self.logger.error("SERVER> Error: short action length")
            self.logger.debug(action)
            self.logger.debug(action_msg)
            self.logger.debug(action)
            self.logger.debug(len(action_msg))
            self.logger.debug(self.action_len)
        conn.close()


def cli():
    """
    Command-line interface to start the server.

    Parses command-line arguments and starts the SQServer with the specified options.
    """
    parser = argparse.ArgumentParser(
        prog='StiQueue Server',
        description='A message queue server')
    parser.add_argument('--debug', action='store_true', help="Showing debug messages")
    parser.add_argument('--host', default="127.0.0.1", help="The host address of the server")
    parser.add_argument('--port', type=int, default=1234, help="The port to listen on")
    parser.add_argument('--buff-size', type=int, help="The size of the buffer")
    args = parser.parse_args()
    if args.debug:
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        logger.addHandler(ch)
    else:
        logger = None
    s = SQServer(host=args.host, port=args.port, logger=logger, buff_size=args.buff_size)
    s.listen()


if __name__ == '__main__':
    cli()
