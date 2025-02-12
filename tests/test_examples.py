import logging
import sys
import unittest
import threading
import multiprocessing
from examples.server_example import SQServer2 as SQServer
from examples.client_example import SQClient2 as SQClient
import os
import time
import random

SLEEP = 0.25

class ExampleTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        host = "127.0.0.1"
        cls.host = host
        avai_port_found = False
        while not avai_port_found:
            cls.port = random.randint(1400, 1500)
            cls.server_process = multiprocessing.Process(target=cls.start_server, args=(host, cls.port))
            cls.server_process.start()
            time.sleep(0.1)
            avai_port_found = cls.server_process.is_alive()

        logger = logging.getLogger(__name__)
        ch = logging.NullHandler()
        logger.addHandler(ch)
        cls.client = SQClient(host=cls.host, port=cls.port, logger=logger)

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
        logger = logging.getLogger(__name__)
        ch = logging.NullHandler()
        logger.addHandler(ch)
        s = SQServer(host=host, port=port, logger=logger)
        s.listen()

    def test_send_and_recv(self):
        client = self.client
        client.enq(b"ABC")
        client.enq(b"DEFG")
        a = client.rev()
        b = client.rev()
        self.assertEqual(a, "CBA")
        self.assertEqual(b, "GFED")


if __name__ == '__main__':
    unittest.main()
