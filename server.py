import socket
from multiprocessing import Lock


class SQServer:

	def __init__(self, host=None, port=1234, wconn=5, max_len=10240, action_len=3):
		self.lock = Lock()
		self.q = []
		self.action_len = action_len
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		if host is None:
			self.host = socket.gethostname()
			print("self host: ")
			print(self.host)
		else:
			self.host = host

		self.port = port
		self.wconn = wconn
		self.socket.bind((self.host, self.port))
		self.max_len = max_len

	def add(self, msg):
		self.q.append(msg)
		print("queue: ")
		print(msg)

	def listen(self):
		while True:
			self.listen_single()

	def listen_single(self):
		action_msg = b""
		self.socket.listen(self.wconn)

		print("Waiting for client...")
		conn, addr = self.socket.accept()  # Accept connection when client connects
		print("Connected by %s" % str(addr))
		while True:
			data = conn.recv(self.max_len)  # Receive client data
			if not data:
				break  # exit from loop if no data
			action_msg += data
			# conn.sendall(data)  # Send the received data back to client
		action = action_msg[:self.action_len]
		msg = ""
		if len(action_msg) > self.action_len:
			msg = action_msg[self.action_len:]
		if action == "add":
			self.add(msg)
		elif action == "get":
			l = len(self.q)
			if l > 0:
				conn.sendall(self.q.pop(0))
		conn.close()


server = SQServer()
server.listen()


# import socket
# host = socket.gethostname()
# port = 12345
# s = socket.socket()		# TCP socket object
# s.bind((host,port))
# s.listen(5)
#
# print "Waiting for client..."
# conn,addr = s.accept()	        # Accept connection when client connects
# print "Connected by ", addr
#
# while True:
# 	data = conn.recv(1024)	    # Receive client data
# 	if not data: break	        # exit from loop if no data
# 	conn.sendall(data)	        # Send the received data back to client
# conn.close()