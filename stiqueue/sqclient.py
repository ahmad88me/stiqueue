import socket
import sys
import time
import logging
import os
from sys import getsizeof


class SQClient:

    def __init__(self, host="127.0.0.1", port=1234, logger=None, buff_size=None):
        self.host = host
        self.port = port
        if host is None:
            self.host = socket.gethostname()
        self.socket = None
        self.buff_size = buff_size
        if logger is None:
            logger = logging.getLogger(__name__)
            # logger.setLevel(logging.CRITICAL)
            # create console handler and set level to debug
            ch = logging.StreamHandler()
            ch.setLevel(logging.DEBUG)
            logger.addHandler(ch)
        self.logger = logger

    def connect(self):
        self.logger.debug("Connecting to %s %d" % (self.host, self.port))
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if self.buff_size:
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, self.buff_size)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, self.buff_size)
        else:
            self.buff_size = self.socket.getsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF)
        self.socket.connect((self.host, self.port))

    def send_with_action(self, msg, action, recv=False):
        total_ret_val = None
        req = action+msg
        self.logger.debug("send with action: ")
        self.logger.debug(req)
        self.connect()
        self.socket.sendall(req)
        if recv:
            # print("\n-------------")
            while True:
                ret_val = self.socket.recv(self.buff_size)
                if total_ret_val is None:
                    total_ret_val = ret_val
                else:
                    total_ret_val += ret_val
                if ret_val in [b'', '']:
                    break
        self.disconnect()
        return total_ret_val

    def enq(self, msg):
        self.send_with_action(msg, b"enq")

    def deq(self):
        return self.send_with_action(b"", b"deq", recv=True)

    def cnt(self):
        return self.send_with_action(b"", b"cnt", recv=True)

    def disconnect(self):
        self.socket.close()


if __name__ == "__main__":
    print("CLIENT is STARTED")
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

    buff_size = None
    if 'stiq_buff_size' in os.environ:
        buff_size = int(os.environ['stiq_buff_size'])

    c = SQClient(host=host, port=port, logger=local_logger)
    for i in range(10):
        print(b"CLIENT> send num %d" % i)
        c.enq(b"num %d" % i)
        # time.sleep(0.2)
    while True:
        time.sleep(1)
        print(b"CLIENT> get num ")
        v = c.deq()
        if v == b"":
            continue
        print("CLIENT: Getting value: %s" % str(v))
