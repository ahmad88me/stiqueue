import socket
import sys
import os
from multiprocessing import Lock


class SQServer:

	def __init__(self, host="127.0.0.1", port=1234, wconn=5, max_len=10240, action_len=3, debug=False):
		self.lock = Lock()
		self.q = []
		self.action_len = action_len
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.debug = debug
		if host is None:
			self.host = socket.gethostname()
			if self.debug:
				print("SERVER> self host: ")
				print(self.host)
		else:
			self.host = host

		self.port = port
		self.wconn = wconn
		self.socket.bind((self.host, self.port))
		self.max_len = max_len
		if self.debug:
			print("SERVER> binded to %s %d" % (self.host, self.port))

	def enq(self, msg):
		print("SERVER> enqueue: ")
		print(msg)
		self.lock.acquire()
		self.q.append(msg)
		self.lock.release()

	def deq(self, conn):
		print("dequeue: ")
		l = len(self.q)
		if l > 0:
			self.lock.acquire()
			v = self.q.pop(0)
			print("SERVER> dequeue: %s" % str(v))
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
		print("other_actions> "+str(action_msg))

	def listen_single(self):
		self.socket.listen(self.wconn)
		if self.debug:
			print("SERVER> Waiting for client...")
		conn, addr = self.socket.accept()  # Accept connection when client connects
		if self.debug:
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
		# print(action_msg)
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
	debug = False
	if 'stiq_debug' in os.environ:
		if os.environ['stiq_debug'].lower() == "true":
			debug = True
			print("SERVER> Debug is on")
	if len(sys.argv) > 2:
		s = SQServer(sys.argv[1], int(sys.argv[2]), debug=debug)
	else:
		if "stiq_host" in os.environ and "stiq_port" in os.environ:
			s = SQServer(host=os.environ['stiq_host'], port=int(os.environ['stiq_port']), debug=debug)
		else:
			s = SQServer(debug=debug)
	s.listen()
