import unittest
from tests.test_client import ClientTest
from tests.test_examples import ExampleTest
from tests.test_client_str_queue import ClientStrQueueTest


def suite():
    suite = unittest.TestSuite()
    suite.addTest(ClientTest)
    suite.addTest(ExampleTest)
    suite.addTest(ClientStrQueueTest)
    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
