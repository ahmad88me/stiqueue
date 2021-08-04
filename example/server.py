from stiqueue.sqserver import SQServer


class SQServer2(SQServer):
    def other_actions(self, action_msg):
        action = action_msg[:self.action_len]
        if len(action_msg) >= self.action_len:
            msg = action_msg[self.action_len:]
            if action == b"rev":
                self.enq(msg[::-1])
            elif action == b"prt":
                print("printing the queue: ")
                for i, msg in enumerate(self.q):
                    print("q(%d)> %s" % (i, msg))
            else:
                print("ERROR: invalid action:")
                print(action_msg)
                print(action)
        else:
            print("Error: invalid action length:")
            print(action_msg)
            print(action)


server = SQServer2()
server.listen()
