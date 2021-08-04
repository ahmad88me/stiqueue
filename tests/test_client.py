import sys
import unittest
import threading
import multiprocessing
from stiqueue.sqserver import SQServer
from stiqueue.sqclient import SQClient
import os
import time
import sys


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
        # t = threading.Thread(target=cls.start_server)
        # t.start()
        # cls.server_thread = t
        time.sleep(1)
        cls.client = SQClient(host=cls.host, port=cls.port)

    @classmethod
    def tearDownClass(cls):
        print("closing things down")
        cls.client.disconnect()
        cls.server_process.terminate()
        # time.sleep(1)
        # sys.exit(0)
        # os._exit(0)
        # cls.server_thread
    # def tearDown(self):
    #     print("closing things down")
    #     self.client.disconnect()
    #     time.sleep(1)
    #     sys.exit(0)
    #     # os._exit(0)

    @classmethod
    def start_server(cls, host, port):
        # host = None
        # port = 1234
        # if 'sqhost' in os.environ:
        #     host = os.environ['sqhost']
        # if 'sqport' in os.environ:
        #     port = int(os.environ['sqport'])
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
        # self.server_process.terminate()
        # self.server_thread._stop
        # sys.exit()
