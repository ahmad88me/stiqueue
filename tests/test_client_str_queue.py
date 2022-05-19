import sys
import unittest
import threading
import multiprocessing
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

for i in range(8):
    long_txt += long_txt


BUFF_SIZE = getsizeof(long_txt) + 10
# print("sizeof: %d" % BUFF_SIZE)


class ClientStrQueueTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        time.sleep(1)
        host = "127.0.0.1"
        port = 1234
        port += 2
        port = random.randint(1300, 1400)
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
        # cls.client = SQClient(host=cls.host, port=cls.port)
        cls.client = SQClient(host=cls.host, port=cls.port, buff_size=BUFF_SIZE)

    @classmethod
    def tearDownClass(cls):
        print("closing things down")
        cls.client.disconnect()
        cls.server_process.terminate()

    @classmethod
    def start_server(cls, host, port):
        s = SQServer(host=host, port=port, str_queue=True, buff_size=BUFF_SIZE)
        s.listen()

    def test_send_and_recv(self):
        self.client = ClientStrQueueTest.client
        self.client.enq("A")
        self.client.enq("B")
        a = self.client.deq()
        b = self.client.deq()
        empty = self.client.deq()
        self.assertEqual(a, "A")
        self.assertEqual(b, "B")
        self.assertEqual(empty, '')


