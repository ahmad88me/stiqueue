import sys
import unittest
import threading
import logging
import multiprocessing
from stiqueue.sqserver import SQServer
from stiqueue.sqclient import SQClient
from queue import SimpleQueue, Queue
from threading import Thread
from multiprocessing import Process, Pipe
import os
import time
import random


SLEEP = 0.25


def deq_thread_func(host, port, pipe_end):
    logger = logging.getLogger(__name__)
    ch = logging.NullHandler()
    logger.addHandler(ch)
    client = SQClient(host=host, port=port, logger=logger, ack_required=False)
    msg = client.deq()
    if pipe_end:
        pipe_end.send(msg)


class ClientNoAckTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        host = "127.0.0.1"
        avai_port_found = False
        while not avai_port_found:
            port = random.randint(1200, 1300)
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
        cls.client = SQClient(host=cls.host, port=cls.port, logger=logger, ack_required=False)


    @classmethod
    def tearDownClass(cls):
        try:
            cls.client.disconnect()
        except:
            pass
        cls.server_process.terminate()

    @classmethod
    def start_server(cls, host, port):
        logger = logging.getLogger(__name__)
        ch = logging.NullHandler()
        logger.addHandler(ch)
        s = SQServer(host=host, port=port, logger=logger, ack_required=False)
        s.listen()

    def test_client_conn_interruption_fail(self):
        client = ClientNoAckTest.client
        host = ClientNoAckTest.host
        port = ClientNoAckTest.port
        p_faulty = Process(target=deq_thread_func, args=(host, port, None))
        p_faulty.start()
        time.sleep(SLEEP)
        p_faulty.terminate()
        client.enq(b"A")
        client.enq(b"B")
        msg = client.deq()
        parent_end, child_end = Pipe()
        p2 = Process(target=deq_thread_func, args=(host, port, child_end))
        p2.start()
        if parent_end.poll(SLEEP):
            msg2 = parent_end.recv()
        else:
            msg2 = None
        p2.join(timeout=SLEEP)
        p2.terminate()
        self.assertEqual(msg, b"B")
        self.assertIsNone(msg2)


if __name__ == '__main__':
    unittest.main()