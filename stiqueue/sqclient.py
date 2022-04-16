import socket
import sys
import time
import logging


class SQClient:

    def __init__(self, host="127.0.0.1", port=1234, max_len=10240, logger=None):
        self.host = host
        self.port = port
        self.max_len = max_len
        if host is None:
            self.host = socket.gethostname()
        self.socket = None
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
        self.socket.connect((self.host, self.port))

    def send_with_action(self, msg, action, recv=False):
        ret_val = None
        req = action+msg
        self.logger.debug("send with action: ")
        self.logger.debug(req)
        self.connect()
        self.socket.send(req)
        if recv:
            ret_val = self.socket.recv(self.max_len)
        self.disconnect()
        return ret_val

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
    c = SQClient(host=host, port=port)
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
