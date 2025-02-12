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

SLEEP = 0.25


class ClientTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        time.sleep(0.2)
        host = "127.0.0.1"
        avai_port_found = False
        while not avai_port_found:
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
            time.sleep(SLEEP)
            avai_port_found = p.is_alive()

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

    def test_peek(self):
        self.client = ClientTest.client
        self.client.enq(b"AA")
        self.client.enq(b"B")
        items = self.client.peek(n=2, sep=",")
        self.assertEqual(items, b"AA,B")
        a = self.client.deq()
        b = self.client.deq()
        self.assertEqual(a, b"AA")
        self.assertEqual(b, b"B")

        self.client.enq(b"CC")
        items = self.client.peek(n=2, sep=",")
        self.assertEqual(items, b"CC")
        self.assertEqual(self.client.deq(), b"CC")

        items = self.client.peek(sep=";")
        self.assertEqual(items, b"")


if __name__ == '__main__':
    unittest.main()