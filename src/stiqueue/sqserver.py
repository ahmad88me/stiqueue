"""
This module implements a simple message queue server.

Classes:
    SQServer: A server that handles enqueuing and dequeuing of messages.

Functions:
    cli: Command-line interface to start the server.
"""

import socket
import traceback
from threading import Thread
import logging
from logging import handlers
import argparse
from queue import SimpleQueue
from TPool import WildPool


class SQServer:
    """
    A simple message queue server that listens for client connections and handing adding (enqueuing) and retrieving
    (dequeuing) of messages.

    Attributes:
        q (queue.SimpleQueue): A list that acts as the message queue.
        action_len (int): Length of the action command in the message.
        socket (socket): The server socket for accepting connections.
        buff_size (int): Buffer size for sending and receiving messages.
        logger (logging.Logger): Logger for debugging and info messages.
        host (str): Host address of the server.
        port (int): Port number to bind the server.
        backlog (int): Maximum number of queued connections.
    """

    def __init__(self, host="127.0.0.1", port=1234, backlog=None, action_len=3, logger=None, buff_size=None,
                 max_workers=5):
        """
        Initializes the SQServer with the specified parameters.

        Args:
            host (str): The host address to bind the server. Defaults to "127.0.0.1".
            port (int): The port number to bind the server. Defaults to 1234.
            backlog (int, optional): Maximum number of queued connections. Defaults to None.
            action_len (int): Length of the action command in the message. Defaults to 3.
            logger (logging.Logger, optional): Logger for logging messages. If None, a default logger is created.
            buff_size (int, optional): Buffer size for sending and receiving messages. Defaults to None.
            max_workers (int): The maximum number of running workers/threads in the TPool.
        """
        self.q = SimpleQueue()
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

        # Using the timeout might make the server stuck if the timeout occur while the lock is acquired
        self.pool = WildPool(logger=logger, pool_size=max_workers)
        self.pool.start_worker()

    def enq(self, msg):
        """
        Enqueues a message into the queue.

        Args:
            msg (bytes): The message to enqueue.
        """
        self.logger.debug("SERVER> enqueue: ")
        self.logger.debug(msg)
        self.q.put(msg, block=False)

    def deq(self, conn):
        """
        Dequeues a message from the queue and sends it to the client.

        Args:
            conn (socket): The client connection to send the message to.
        """
        self.logger.debug("SERVER> Spawning a dequeue thread ... ")
        th = Thread(target=self._blocking_deq, args=(conn,))
        self.pool.add_thread(th)

    def _blocking_deq(self, conn):
        """
        Dequeues a message from the queue and sends it to the client.

        Args:
            conn (socket): The client connection to send the message to.
        """
        try:
            self.logger.debug("SERVER> Waiting for the queue ... ")
            msg = self.q.get(block=True)
            self.logger.debug("SERVER> dequeue: %s" % str(msg))
            conn.sendall(msg)

        except Exception as e:
            self.logger.error(f"SERVER> exception in blocking deq: {e}")
            self.logger.error(traceback.format_exc())
            self.logger.error(f"SERVER> Adding the msg again to the queue. {msg}")
            self.enq(msg)
        finally:
            self.logger.debug("SERVER> closing connection: %s" % str(conn))
            conn.close()

    def cnt(self, conn):
        """
        Sends the count of messages in the queue to the client.

        Args:
            conn (socket): The client connection to send the count to.
        """
        b = b'%d' % self.q.qsize()
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
        close_conn = True
        self.logger.debug("SERVER> Waiting for client...")
        conn, addr = self.socket.accept()  # Accept connection when client connects
        self.logger.debug("SERVER> Connected by %s" % str(addr))
        # action_msg = conn.recv(self.buff_size)  # Receive client data
        action_msg = b""
        while True:
            recv_data = conn.recv(self.buff_size)  # Receive client data
            if recv_data:
                action_msg += recv_data
                if len(recv_data) < self.buff_size:
                    break
            else:
                break
        action = action_msg[:self.action_len]
        if len(action_msg) >= self.action_len:
            msg = action_msg[self.action_len:]
            if action == b"enq":
                self.enq(msg)
            elif action == b"deq":
                self.deq(conn)
                close_conn = False
            elif action == b"cnt":
                self.cnt(conn)
            else:
                self.logger.debug("SERVER> other action: ")
                self.logger.debug(action)
                self.other_actions(action_msg)
        else:
            self.logger.error("SERVER> Error: short action length")
            self.logger.error(action)
            self.logger.error(action_msg)
            self.logger.error(len(action_msg))
            self.logger.error(self.action_len)
        if close_conn:
            self.logger.debug(f"SERVER> Closing connection from listen single {conn}")
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
    parser.add_argument('--log', help="The log file")

    args = parser.parse_args()
    logger = logging.getLogger(__name__)
    if args.log:
        ch = handlers.RotatingFileHandler(args.log)
    else:
        ch = logging.StreamHandler()
    if args.debug:
        logger.setLevel(logging.DEBUG)
        ch.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)
        ch.setLevel(logging.INFO)
    logger.addHandler(ch)

    # if args.debug:
    #     logger = logging.getLogger(__name__)
    #     logger.setLevel(logging.DEBUG)
    #     ch = logging.StreamHandler()
    #     ch.setLevel(logging.DEBUG)
    #     logger.addHandler(ch)
    # else:
    #     logger = None
    s = SQServer(host=args.host, port=args.port, logger=logger, buff_size=args.buff_size)
    s.listen()


if __name__ == '__main__':
    cli()
