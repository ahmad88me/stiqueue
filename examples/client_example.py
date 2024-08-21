import logging
from stiqueue import SQClient


class SQClient2(SQClient):

    def rev(self):
        msg = self.send_with_action(msg=b"", action=b"deq", recv=True)
        msg = msg.decode()
        return msg[::-1]


def get_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    logger.addHandler(ch)
    return logger


def main(logger=None):
    if logger is None:
        logger = get_logger()

    p1 = SQClient2()
    p2 = SQClient2()
    p1.enq(b"P1> This is message one")
    p1.enq(b"P2> This is message two")
    p2.enq(b"P2> This is message three")
    logger.debug("get from P1: ")
    msg = p1.deq()
    logger.debug(f"msg1: {msg}")
    msg = p1.rev()
    logger.debug(f"msg2 rev: {msg}")
    logger.debug("get from P2: ")
    msg = p2.rev()
    logger.debug(f"msg3 rev: {msg}")


if __name__ == '__main__':
    main()