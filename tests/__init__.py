import unittest
from tests.test_client import ClientTest
from tests.test_examples import ExampleTest


def suite():
    suite = unittest.TestSuite()
    suite.addTest(ClientTest)
    suite.addTest(ExampleTest)
    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())