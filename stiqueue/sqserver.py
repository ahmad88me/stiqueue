import socket
import sys
import os
from multiprocessing import Lock
import logging


class SQServer:

    def __init__(self, host="127.0.0.1", port=1234, wconn=5, action_len=3, str_queue=False, debug=False,
                 debug_wait=False, logger=None, buff_size=None):
        self.lock = Lock()
        self.q = []
        self.action_len = action_len
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.debug = debug
        self.debug_wait = debug_wait
        self.str_queue = str_queue
        if buff_size:
            self.buff_size = buff_size
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, buff_size)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, buff_size)
        else:
            self.buff_size = self.socket.getsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, self.buff_size)

        if not logger:
            logger = logging.getLogger(__name__)
            # logger.setLevel(logging.CRITICAL)
            # create console handler and set level to debug
            ch = logging.StreamHandler()
            ch.setLevel(logging.INFO)
            logger.addHandler(ch)
        self.logger = logger
        if host is None:
            self.host = socket.gethostname()
            if self.debug:
                self.logger.debug("SERVER> self host: ")
                self.logger.debug(self.host)
        else:
            self.host = host

        self.port = port
        self.wconn = wconn
        self.socket.bind((self.host, self.port))
        if self.debug:
            self.logger.debug("SERVER> binded to %s %d" % (self.host, self.port))

    def enq(self, msg):
        if self.debug:
            self.logger.debug("SERVER> enqueue: ")
            self.logger.debug(msg)
        self.lock.acquire()
        if self.str_queue:
            dec_msg = msg.decode()
            self.q.append(dec_msg)
        else:
            self.q.append(msg)
        self.lock.release()

    def deq(self, conn):
        self.lock.acquire()
        if len(self.q) > 0:
            v = self.q.pop(0)
            if self.str_queue:
                v = v.encode()
            self.logger.debug("SERVER> dequeue: %s" % str(v))
            conn.sendall(v)
        self.lock.release()

    def cnt(self, conn):
        b = b'%d' % len(self.q)
        conn.sendall(b)

    def listen(self):
        while True:
            self.listen_single()

    def other_actions(self, action_msg):
        """
        :param action_msg:
        :return:
        """
        if self.debug:
            self.logger.debug("other_actions> " + str(action_msg))

    def listen_single(self):
        self.socket.listen(self.wconn)
        if self.debug_wait:
            self.logger.debug("SERVER> Waiting for client...")
        conn, addr = self.socket.accept()  # Accept connection when client connects
        if self.debug_wait:
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
                if self.debug:
                    self.logger.debug("SERVER> other action: ")
                    self.logger.debug(action)
                self.other_actions(action_msg)
        else:
            self.logger.error("SERVER> Error: short action length")
            self.logger.debug(action)
            if self.debug:
                self.logger.debug(action_msg)
                self.logger.debug(action)
                self.logger.debug(len(action_msg))
                self.logger.debug(self.action_len)
        conn.close()


if __name__ == '__main__':
    debug = False
    if 'stiq_debug' in os.environ:
        if os.environ['stiq_debug'].lower() == "true":
            debug = True
            print("SERVER> Debug is on")
    buff_size = None
    if 'stiq_buff_size' in os.environ:
        buff_size = int(os.environ['stiq_buff_size'])
    if len(sys.argv) > 2:
        s = SQServer(sys.argv[1], int(sys.argv[2]), debug=debug, buff_size=buff_size)
    else:
        if "stiq_host" in os.environ and "stiq_port" in os.environ:
            s = SQServer(host=os.environ['stiq_host'], port=int(os.environ['stiq_port']), debug=debug,
                         buff_size=buff_size)
        else:
            s = SQServer(debug=debug, buff_size=buff_size)
    s.listen()
