import sys
import unittest
import threading
import multiprocessing
from stiqueue.sqserver import SQServer
from stiqueue.sqclient import SQClient
import os
import time


class ClientTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        time.sleep(1)
        host = None
        port = 1234
        if 'sqhost' in os.environ:
            host = os.environ['sqhost']
        if 'sqport' in os.environ:
            port = int(os.environ['sqport'])
        cls.host = host
        cls.port = port
        p = multiprocessing.Process(target=cls.start_server, args=(host, port))
        p.start()
        cls.server_process = p
        time.sleep(1)
        cls.client = SQClient(host=cls.host, port=cls.port)

    @classmethod
    def tearDownClass(cls):
        print("closing things down")
        cls.client.disconnect()
        cls.server_process.terminate()

    @classmethod
    def start_server(cls, host, port):
        s = SQServer(host=host, port=port)
        s.listen()

    def test_send_and_recv(self):
        self.client = ClientTest.client
        self.client.enq(b"A")
        self.client.enq(b"B")
        a = self.client.deq()
        b = self.client.deq()
        empty = self.client.deq()
        self.assertEqual(a, b"A")
        self.assertEqual(b, b"B")
        self.assertEqual(empty, b'')

