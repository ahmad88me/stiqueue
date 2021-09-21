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
			print("SERVER> self host: ")
			print(self.host)
		else:
			self.host = host

		self.port = port
		self.wconn = wconn
		self.socket.bind((self.host, self.port))
		self.max_len = max_len

	def enq(self, msg):
		print("SERVER> enqueue: ")
		print(msg)
		self.lock.acquire()
		self.q.append(msg)
		self.lock.release()

	def deq(self, conn):
		# print("dequeue: ")
		l = len(self.q)
		if l > 0:
			self.lock.acquire()
			v = self.q.pop(0)
			print("SERVER> dequeue: %s" % str(v))
			conn.sendall(v)
			self.lock.release()

	def listen(self):
		while True:
			self.listen_single()

	def other_actions(self, action_msg):
		"""
		:param action_msg:
		:return:
		"""
		print("other_actions> "+str(action_msg))

	def listen_single(self):
		self.socket.listen(self.wconn)
		print("SERVER> Waiting for client...")
		conn, addr = self.socket.accept()  # Accept connection when client connects
		print("SERVER> Connected by %s" % str(addr))
		action_msg = conn.recv(self.max_len)  # Receive client data
		# print("DEBUG: action msg: ")
		# while True:
		# 	data = conn.recv(self.max_len)  # Receive client data
		# 	if not data:
		# 		break  # exit from loop if no data
		# 	action_msg += data
		# 	# conn.sendall(data)  # Send the received data back to client
		# print("DEBUG: action msg: ")
		print(action_msg)
		action = action_msg[:self.action_len]
		if len(action_msg) >= self.action_len:
			msg = action_msg[self.action_len:]
			if action == b"enq":
				self.enq(msg)
			elif action == b"deq":
				self.deq(conn)
			else:
				print("SERVER> other action: ")
				print(action)
				self.other_actions(action_msg)
		else:
			print("SERVER> Error: short action length: ")
			print(action_msg)
			print(action)
			print(len(action_msg))
			print(self.action_len)
		conn.close()


if __name__ == '__main__':
	s = SQServer()
	s.listen()