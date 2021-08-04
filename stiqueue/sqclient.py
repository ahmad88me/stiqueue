import socket


class SQClient:

    def __init__(self, host=None, port=1234, max_len=10240):
        self.host = host
        self.port = port
        self.max_len = max_len
        if host is None:
            self.host = socket.gethostname()
        self.socket = None

    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))

    def send_with_action(self, msg, action, recv=False):
        ret_val = None
        req = action+msg
        # print("send with action: ")
        # print(req)
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

    def disconnect(self):
        self.socket.close()
