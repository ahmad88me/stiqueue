import socket
import sys
from multiprocessing import Lock
import logging

class SQServer:

	def __init__(self, host="127.0.0.1", port=1234, wconn=5, max_len=10240, action_len=3, logger=None):
		if logger is None:
			logger = logging.getLogger(__name__)
			# logger.setLevel(logging.CRITICAL)
			# create console handler and set level to debug
			ch = logging.StreamHandler()
			ch.setLevel(logging.INFO)
			logger.addHandler(ch)
		self.logger = logger
		self.lock = Lock()
		self.q = []
		self.action_len = action_len
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		if host is None:
			self.host = socket.gethostname()
			self.logger.debug("SERVER> self host: ")
			print(self.host)
		else:
			self.host = host

		self.port = port
		self.wconn = wconn
		self.socket.bind((self.host, self.port))
		self.max_len = max_len

	def enq(self, msg):
		self.logger.debug("SERVER> enqueue: ")
		self.logger.debug(msg)
		self.lock.acquire()
		self.q.append(msg)
		self.lock.release()

	def deq(self, conn):
		l = len(self.q)
		if l > 0:
			self.lock.acquire()
			v = self.q.pop(0)
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
		self.logger.debug("other_actions> "+str(action_msg))

	def listen_single(self):
		self.socket.listen(self.wconn)
		self.logger.debug("SERVER> Waiting for client...")
		conn, addr = self.socket.accept()  # Accept connection when client connects
		self.logger.debug("SERVER> Connected by %s" % str(addr))
		action_msg = conn.recv(self.max_len)  # Receive client data
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
			self.logger.debug("SERVER> Error: short action length: ")
			self.logger.debug(action_msg)
			self.logger.debug(action)
			self.logger.debug(len(action_msg))
			self.logger.debug(self.action_len)
		conn.close()


if __name__ == '__main__':
	if len(sys.argv) > 2:
		s = SQServer(sys.argv[1], int(sys.argv[2]))
	else:
		s = SQServer()
	s.listen()
