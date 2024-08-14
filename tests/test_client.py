import sys
import unittest
import threading
import logging
import multiprocessing
from stiqueue.sqserver import SQServer
from stiqueue.sqclient import SQClient
import os
import time
import random


class ClientTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        time.sleep(1)
        host = "127.0.0.1"
        port = 1234
        port = random.randint(1200, 1300)
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
        logger = logging.getLogger(__name__)
        ch = logging.NullHandler()
        logger.addHandler(ch)
        cls.client = SQClient(host=cls.host, port=cls.port, logger=logger)

    @classmethod
    def tearDownClass(cls):
        cls.client.disconnect()
        cls.server_process.terminate()

    @classmethod
    def start_server(cls, host, port):
        logger = logging.getLogger(__name__)
        ch = logging.NullHandler()
        logger.addHandler(ch)
        s = SQServer(host=host, port=port, logger=logger)
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


if __name__ == '__main__':
    unittest.main()