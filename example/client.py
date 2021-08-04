from stiqueue.sqclient import SQClient


class SQClient2(SQClient):

    def prt(self):
        return self.send_with_action(b"", b"prt")

    def rev(self, msg):
        return self.send_with_action(msg, b"deq")


p1 = SQClient2()
p2 = SQClient2()
p1.enq(b"P1> This is message one")
p1.enq(b"P2> This is message two")
p2.enq(b"P2> This is two")
print("get from P1: ")
msg = p1.deq()
print("msg1: ")
print(msg)
msg = p1.deq()
print("msg2: ")
print(msg)
print("get from P2: ")
msg = p2.deq()
print("msg4: ")
print(msg)
msg = p2.deq()
print("msg2: (should be empty)")
print(msg)
msg = p1.deq()
print("msg3: (should be empty)")
print(msg)
p1.prt()
p2.prt()