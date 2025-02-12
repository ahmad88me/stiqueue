import sys
import unittest
import threading
import multiprocessing
import logging
from stiqueue.sqserver import SQServer
from stiqueue.sqclient import SQClient
import os
import time
import random
from sys import getsizeof


long_txt = """
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Praesent cursus dolor sed tincidunt malesuada. In malesuada,
metus at suscipit ullamcorper, ante felis consequat risus, sed dignissim ante nisl volutpat leo. Vivamus eleifend justo 
sed quam molestie pharetra. Duis blandit orci finibus eros faucibus porta. Pellentesque massa massa, aliquet sit amet 
posuere vitae, eleifend eget nibh. Morbi lacus odio, elementum vitae nunc vel, finibus placerat augue. Nam tincidunt 
dui diam. Nunc rutrum vel sapien nec consequat. Quisque pellentesque, sem in auctor facilisis, metus sem euismod arcu,
 at vehicula purus est vel justo. Curabitur quis elit tellus. Ut commodo justo non urna tempor, ut semper eros 
 malesuada.

Nulla bibendum odio sed augue varius, ut sodales lorem facilisis. Suspendisse non metus vitae nisl tincidunt ornare.
 Curabitur semper placerat ligula convallis finibus. Pellentesque ornare ut quam non porta. Nam sed rutrum ipsum. Cras 
 tempor efficitur nisl, pulvinar volutpat augue justo.
"""

for i in range(3):
    long_txt += long_txt


class ClientStrQueueLongTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        host = "127.0.0.1"
        cls.host = host
        avai_port_found = False
        while not avai_port_found:
            port = random.randint(1500, 1600)
            cls.port = port
            p = multiprocessing.Process(target=cls.start_server, args=(host, port))
            p.start()
            cls.server_process = p
            time.sleep(0.1)
            avai_port_found = p.is_alive()

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

    def test_send_and_recv_long(self):
        self.client = ClientStrQueueLongTest.client
        self.client.enq(long_txt.encode())
        self.client.enq(b"B")
        a = self.client.deq().decode()
        b = self.client.deq().decode()
        self.assertEqual(a[:100], long_txt[:100])
        self.assertEqual(len(a), len(long_txt))
        self.assertEqual(a, long_txt)
        self.assertEqual(b, "B")


if __name__ == '__main__':
    unittest.main()
