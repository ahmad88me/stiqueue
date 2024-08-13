import sys
import unittest
import threading
import multiprocessing
from example.server import SQServer2 as SQServer
from example.client import SQClient2 as SQClient
import os
import time
import random


class ExampleTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        host = "127.0.0.1"
        port = random.randint(1400, 1500)
        if 'sqhost' in os.environ:
            host = os.environ['sqhost']
        if 'sqport' in os.environ:
            port = int(os.environ['sqport'])
        cls.host = host
        cls.port = port + 1

        cls.server_process = multiprocessing.Process(target=cls.start_server, args=(host, cls.port))
        cls.server_process.start()
        time.sleep(0.1)  # Give the server time to start

        cls.client = SQClient(host=cls.host, port=cls.port)

    @classmethod
    def tearDownClass(cls):
        cls.client.disconnect()
        cls.server_process.terminate()
        cls.server_process.join()
        for child in multiprocessing.active_children():
            child.terminate()
            child.join()

    @classmethod
    def start_server(cls, host, port):
        s = SQServer(host=host, port=port)
        s.listen()

    def test_send_and_recv(self):
        client = self.client
        client.enq(b"A")
        client.enq(b"B")
        a = client.deq()
        b = client.deq()
        empty = client.deq()
        self.assertEqual(a, b"A")
        self.assertEqual(b, b"B")
        self.assertEqual(empty, b'')


if __name__ == '__main__':
    unittest.main()
