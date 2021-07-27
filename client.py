import socket


class SQClient:

    def __init__(self, host=None, port=1234, connect=False, max_len=10240):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.port = port
        self.max_len = max_len
        if host is None:
            self.host = socket.gethostname()
        if connect:
            self.socket.connect((self.host, self.port))

    def connect(self):
        self.socket.connect((self.host, self.port))

    def send_with_action(self, msg, action):
        req = action+msg
        print("send with action")
        print(req)
        self.socket.sendall(req)

    def add(self, msg):
        self.send_with_action(msg, b"add")

    def get(self):
        return self.send_with_action(b"", b"get")

    def close(self):
        self.socket.close()


p1 = SQClient(connect=True)
p2 = SQClient(connect=True)
p1.add(b"P1> This is message one")
p2.add(b"P2> This is two")
# p1.close()
# p2.close()
print("results: ")
msg = p1.get()
print("msg1: ")
print(msg)
msg = p1.get()
print("msg2: ")
print(msg)
